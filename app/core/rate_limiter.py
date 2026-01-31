"""
Rate Limiter Module
API rate limiting to prevent abuse.
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from collections import defaultdict
import asyncio

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.config import settings


class RateLimiter:
    """
    In-memory rate limiter using sliding window algorithm.
    For production, use Redis-based implementation.
    """
    
    def __init__(
        self,
        requests_per_period: int = 100,
        period_seconds: int = 60,
    ):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_period: Maximum requests allowed per period
            period_seconds: Time period in seconds
        """
        self.requests_per_period = requests_per_period
        self.period_seconds = period_seconds
        self._requests: Dict[str, list] = defaultdict(list)
        self._lock = asyncio.Lock()
    
    def _get_client_id(self, request: Request) -> str:
        """
        Extract client identifier from request.
        Uses IP address and optionally user ID.
        """
        # Get IP from headers (for proxied requests) or direct connection
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"
        
        # Include user ID if authenticated
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"{ip}:{user_id}"
        
        return ip
    
    def _clean_old_requests(self, client_id: str) -> None:
        """Remove requests outside the current time window."""
        cutoff = datetime.utcnow() - timedelta(seconds=self.period_seconds)
        self._requests[client_id] = [
            ts for ts in self._requests[client_id]
            if ts > cutoff
        ]
    
    async def is_allowed(self, request: Request) -> Tuple[bool, Dict]:
        """
        Check if request is allowed under rate limit.
        
        Args:
            request: FastAPI request object
        
        Returns:
            Tuple of (is_allowed, rate_limit_info)
        """
        async with self._lock:
            client_id = self._get_client_id(request)
            now = datetime.utcnow()
            
            # Clean expired entries
            self._clean_old_requests(client_id)
            
            # Count requests in current window
            request_count = len(self._requests[client_id])
            
            # Calculate remaining requests
            remaining = max(0, self.requests_per_period - request_count)
            
            # Calculate reset time
            if self._requests[client_id]:
                oldest = min(self._requests[client_id])
                reset_at = oldest + timedelta(seconds=self.period_seconds)
            else:
                reset_at = now + timedelta(seconds=self.period_seconds)
            
            info = {
                "limit": self.requests_per_period,
                "remaining": remaining,
                "reset_at": reset_at.isoformat(),
            }
            
            if request_count >= self.requests_per_period:
                return False, info
            
            # Record this request
            self._requests[client_id].append(now)
            info["remaining"] = remaining - 1
            
            return True, info


# Global rate limiter instances
default_limiter = RateLimiter(
    requests_per_period=settings.RATE_LIMIT_REQUESTS,
    period_seconds=settings.RATE_LIMIT_PERIOD,
)

# Stricter limiter for auth endpoints
auth_limiter = RateLimiter(
    requests_per_period=10,
    period_seconds=60,
)

# Very strict limiter for sensitive operations
sensitive_limiter = RateLimiter(
    requests_per_period=5,
    period_seconds=300,
)


async def rate_limit_middleware(
    request: Request,
    limiter: Optional[RateLimiter] = None,
) -> None:
    """
    Rate limiting middleware function.
    
    Args:
        request: FastAPI request
        limiter: Rate limiter instance to use
    
    Raises:
        HTTPException: If rate limit exceeded
    """
    if limiter is None:
        limiter = default_limiter
    
    allowed, info = await limiter.is_allowed(request)
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "limit": info["limit"],
                "reset_at": info["reset_at"],
            },
            headers={
                "X-RateLimit-Limit": str(info["limit"]),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": info["reset_at"],
                "Retry-After": str(settings.RATE_LIMIT_PERIOD),
            },
        )


def rate_limit(limiter: Optional[RateLimiter] = None):
    """
    Dependency for rate limiting individual routes.
    
    Usage:
        @app.get("/api/resource")
        async def get_resource(
            _: None = Depends(rate_limit(auth_limiter))
        ):
            ...
    """
    async def dependency(request: Request):
        await rate_limit_middleware(request, limiter)
    
    return dependency
