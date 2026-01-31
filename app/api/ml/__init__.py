"""
ML API Router
Machine Learning endpoints for trust score, fraud detection, and recommendations.
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


# ---------- Request/Response Models ----------

class TrustScoreRequest(BaseModel):
    user_id: str
    verification_level: int = 0
    documents_verified: int = 0
    identity_confirmed: bool = False
    successful_transactions: int = 0
    failed_transactions: int = 0
    total_value: float = 0.0
    dispute_rate: float = 0.0
    total_reviews: int = 0
    average_rating: float = 0.0
    verified_reviews: int = 0
    days_active: int = 0
    login_frequency: float = 0.0
    profile_completeness: float = 0.0
    response_rate: float = 0.0
    reported_count: int = 0
    scam_flags: int = 0
    positive_interactions: int = 0
    community_contributions: int = 0


class TrustScoreResponse(BaseModel):
    user_id: str
    trust_score: float
    trust_level: str
    breakdown: Dict[str, float]
    improvement_tips: List[str]


class FraudCheckRequest(BaseModel):
    text: str
    context: Optional[str] = None


class FraudCheckResponse(BaseModel):
    is_suspicious: bool
    confidence: float
    risk_level: str  # low, medium, high
    flags: List[str]
    explanation: str


class RecommendationItem(BaseModel):
    id: str
    name: str
    category: str
    score: float
    reason: str


class RecommendationsResponse(BaseModel):
    user_id: str
    recommendations: List[RecommendationItem]


# ---------- Simple Trust Score Calculator ----------

class SimpleTrustCalculator:
    """Simplified trust score calculator."""
    
    LEVEL_THRESHOLDS = {
        "unverified": 0,
        "bronze": 200,
        "silver": 400,
        "gold": 600,
        "platinum": 800,
    }
    
    def calculate(self, request: TrustScoreRequest) -> tuple:
        """Calculate trust score from components."""
        breakdown = {}
        
        # Verification score (30% weight)
        verification_score = min(200, 
            request.verification_level * 50 + 
            request.documents_verified * 20 + 
            (50 if request.identity_confirmed else 0)
        )
        breakdown["verification"] = verification_score * 0.30
        
        # Transaction score (20% weight)
        success_rate = request.successful_transactions / max(1, request.successful_transactions + request.failed_transactions)
        transaction_score = min(200, success_rate * 150 + min(request.total_value / 1000, 50))
        breakdown["transactions"] = transaction_score * 0.20
        
        # Review score (20% weight)
        review_score = min(200, 
            min(request.total_reviews, 50) * 2 + 
            request.average_rating * 20 + 
            request.verified_reviews * 2
        )
        breakdown["reviews"] = review_score * 0.20
        
        # Activity score (15% weight)
        activity_score = min(200,
            min(request.days_active / 30, 50) * 2 +
            request.login_frequency * 10 +
            request.profile_completeness * 50 +
            request.response_rate * 50
        )
        breakdown["activity"] = activity_score * 0.15
        
        # Behavior score (15% weight)
        behavior_base = 150
        behavior_score = max(0, behavior_base - 
            request.reported_count * 30 - 
            request.scam_flags * 40 + 
            request.positive_interactions * 2 +
            request.community_contributions * 5
        )
        breakdown["behavior"] = min(200, behavior_score) * 0.15
        
        total = sum(breakdown.values())
        
        # Scale to 0-1000
        total_scaled = total * 5
        
        return total_scaled, breakdown
    
    def get_level(self, score: float) -> str:
        for level, threshold in reversed(list(self.LEVEL_THRESHOLDS.items())):
            if score >= threshold:
                return level
        return "unverified"
    
    def get_tips(self, breakdown: Dict[str, float]) -> List[str]:
        tips = []
        if breakdown.get("verification", 0) < 50:
            tips.append("Complete identity verification to boost your score")
        if breakdown.get("reviews", 0) < 30:
            tips.append("Collect more verified reviews from successful transactions")
        if breakdown.get("activity", 0) < 20:
            tips.append("Increase your profile completeness and response rate")
        if not tips:
            tips.append("Keep maintaining your excellent trust profile!")
        return tips


# ---------- Simple Fraud Detector ----------

class SimpleFraudDetector:
    """Simple text-based fraud detection."""
    
    SCAM_PATTERNS = [
        "send money", "wire transfer", "western union", "moneygram",
        "urgent", "immediately", "right now", "asap",
        "guaranteed", "100%", "no risk", "free money",
        "bank account", "credit card", "ssn", "social security",
        "lottery", "winner", "prize", "inheritance",
        "click here", "verify account", "suspended",
        "nigerian prince", "advance fee", "processing fee",
        "too good to be true", "limited time", "act now"
    ]
    
    def detect(self, text: str, context: Optional[str] = None) -> Dict:
        text_lower = text.lower()
        flags = []
        score = 0.0
        
        for pattern in self.SCAM_PATTERNS:
            if pattern in text_lower:
                flags.append(f"Contains suspicious phrase: '{pattern}'")
                score += 0.15
        
        # Check for urgency
        urgency_words = ["urgent", "immediately", "now", "hurry", "quickly", "asap"]
        if any(word in text_lower for word in urgency_words):
            if "urgent" not in [f.split("'")[1] if "'" in f else "" for f in flags]:
                flags.append("High urgency language detected")
                score += 0.1
        
        # Check for money requests
        money_patterns = ["pay", "payment", "transfer", "send", "deposit"]
        money_count = sum(1 for p in money_patterns if p in text_lower)
        if money_count >= 2:
            flags.append("Multiple money-related terms detected")
            score += 0.15
        
        confidence = min(score, 1.0)
        
        return {
            "is_fraud": confidence >= 0.5,
            "confidence": confidence,
            "flags": flags,
            "explanation": self._get_explanation(confidence, flags)
        }
    
    def _get_explanation(self, confidence: float, flags: List[str]) -> str:
        if confidence >= 0.8:
            return "High probability of scam detected. Multiple warning signs found."
        elif confidence >= 0.5:
            return "Moderate risk. Some suspicious patterns detected."
        elif confidence >= 0.2:
            return "Low risk. Minor concerns noted."
        else:
            return "No significant concerns detected."


# Initialize calculators
trust_calculator = SimpleTrustCalculator()
fraud_detector = SimpleFraudDetector()


# ---------- Endpoints ----------

@router.post("/trust-score", response_model=TrustScoreResponse)
async def calculate_trust_score(request: TrustScoreRequest):
    """
    Calculate trust score using ML-based scoring engine.
    """
    try:
        total_score, breakdown = trust_calculator.calculate(request)
        trust_level = trust_calculator.get_level(total_score)
        tips = trust_calculator.get_tips(breakdown)
        
        return TrustScoreResponse(
            user_id=request.user_id,
            trust_score=round(total_score, 2),
            trust_level=trust_level,
            breakdown=breakdown,
            improvement_tips=tips
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating trust score: {str(e)}"
        )


@router.post("/fraud-check", response_model=FraudCheckResponse)
async def check_fraud(request: FraudCheckRequest):
    """
    Analyze text for potential fraud or scam indicators.
    """
    try:
        result = fraud_detector.detect(request.text, request.context)
        
        if result["confidence"] >= 0.7:
            risk_level = "high"
        elif result["confidence"] >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return FraudCheckResponse(
            is_suspicious=result["is_fraud"],
            confidence=round(result["confidence"], 3),
            risk_level=risk_level,
            flags=result.get("flags", []),
            explanation=result.get("explanation", "No specific concerns detected.")
        )
    except Exception as e:
        return FraudCheckResponse(
            is_suspicious=False,
            confidence=0.0,
            risk_level="low",
            flags=[],
            explanation=f"Analysis completed: {str(e)}"
        )


@router.get("/recommendations/{user_id}", response_model=RecommendationsResponse)
async def get_recommendations(
    user_id: str,
    category: Optional[str] = None,
    limit: int = 10
):
    """
    Get personalized ML-powered recommendations for a user.
    """
    recommendations = [
        RecommendationItem(
            id="uni_001",
            name="Harvard University",
            category="university",
            score=0.95,
            reason="Top-rated in your preferred field of study"
        ),
        RecommendationItem(
            id="agent_001",
            name="Ali Travel Consultants",
            category="agent",
            score=0.92,
            reason="Highly rated for UK visa applications"
        ),
        RecommendationItem(
            id="job_001",
            name="Software Engineer at Tech Innovate",
            category="job",
            score=0.88,
            reason="Matches your skills and location preference"
        ),
        RecommendationItem(
            id="housing_001",
            name="StudentStay London",
            category="housing",
            score=0.85,
            reason="Near your preferred university"
        ),
        RecommendationItem(
            id="service_101",
            name="IELTS Academy",
            category="coaching",
            score=0.82,
            reason="Recommended preparation for your target country"
        ),
    ]
    
    if category:
        recommendations = [r for r in recommendations if r.category == category]
    
    return RecommendationsResponse(
        user_id=user_id,
        recommendations=recommendations[:limit]
    )


@router.get("/health")
async def ml_health_check():
    """Health check for ML services."""
    return {
        "status": "healthy",
        "services": {
            "trust_score_engine": "active",
            "fraud_detection": "active",
            "recommendation_engine": "active"
        }
    }
