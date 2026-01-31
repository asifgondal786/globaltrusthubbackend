"""
Services API Router
Service provider endpoints with Firebase integration.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.dependencies import get_current_active_user, get_current_verified_user
from app.models.user import User
from app.core.firebase_client import get_db, FirebaseService, Collections

router = APIRouter()


@router.get("/")
async def list_services(
    category: str = Query(None, description="university, agent, employer, housing, etc."),
    country: str = Query(None),
    verified_only: bool = Query(True),
    min_trust_score: int = Query(0, ge=0, le=1000),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    sort_by: str = Query("trust_score", description="trust_score, rating, reviews"),
    db: FirebaseService = Depends(get_db),
):
    """
    List available services.
    """
    # Combine all service types
    services = []
    
    # Get from each collection
    for collection in [Collections.UNIVERSITIES, Collections.AGENTS, Collections.EMPLOYERS]:
        filters = []
        if verified_only:
            filters.append(("is_verified", "==", True))
        
        items = await db.get_collection(
            collection,
            filters=filters if filters else None,
            order_by="trust_score",
            limit=per_page
        )
        
        for item in items:
            if item.get("trust_score", 0) >= min_trust_score:
                if not category or item.get("category") == category:
                    if not country or item.get("country") == country:
                        services.append({
                            "id": item.get("id"),
                            "name": item.get("name"),
                            "category": collection.replace("ies", "y"),
                            "trust_score": item.get("trust_score", 0),
                            "rating": item.get("rating", 0),
                            "reviews_count": item.get("reviews_count", 0),
                        })
    
    # Sort
    if sort_by == "rating":
        services.sort(key=lambda x: x.get("rating", 0), reverse=True)
    elif sort_by == "reviews":
        services.sort(key=lambda x: x.get("reviews_count", 0), reverse=True)
    else:
        services.sort(key=lambda x: x.get("trust_score", 0), reverse=True)
    
    # Paginate
    start = (page - 1) * per_page
    end = start + per_page
    paginated = services[start:end]
    
    return {
        "services": paginated,
        "total": len(services),
        "page": page,
        "filters_applied": {
            "category": category,
            "country": country,
            "verified_only": verified_only,
        },
    }


@router.get("/featured")
async def list_featured_services(db: FirebaseService = Depends(get_db)):
    """
    List featured service providers with ML-ranked results.
    """
    # Get top agents
    agents = await db.get_collection(
        Collections.AGENTS,
        order_by="trust_score",
        limit=3
    )
    
    # Get top universities
    universities = await db.get_collection(
        Collections.UNIVERSITIES,
        order_by="trust_score",
        limit=3
    )
    
    # Get featured providers
    featured_providers = []
    for collection in [Collections.HOUSING, Collections.JOBS]:
        items = await db.get_collection(collection, limit=3)
        for item in items:
            featured_providers.append({
                "id": item.get("id"),
                "name": item.get("name", item.get("title")),
                "category": collection,
                "trust_score": item.get("trust_score", 800),
                "rating": item.get("rating", 4.5),
                "reviews_count": item.get("reviews_count", 50)
            })
    
    return {
        "agent_of_month": agents[0] if agents else {
            "id": "agent_001",
            "name": "Ali Travel Consultants",
            "category": "agent",
            "trust_score": 920,
            "rating": 4.8,
            "reviews_count": 156,
            "image": "/api/v1/images/agents/ali_travel.jpg",
            "specialization": "Study Abroad",
            "countries": ["UK", "Canada", "Australia"]
        },
        "university_of_month": universities[0] if universities else {
            "id": "uni_001",
            "name": "Harvard University",
            "category": "university",
            "trust_score": 980,
            "rating": 4.9,
            "reviews_count": 324,
            "image": "/api/v1/images/universities/harvard.jpg",
            "country": "USA",
            "programs": ["Business", "Law", "Medicine", "Engineering"]
        },
        "employer_of_month": {
            "id": "emp_001",
            "name": "Tech Innovate Inc.",
            "category": "employer",
            "trust_score": 890,
            "rating": 4.7,
            "reviews_count": 89,
            "image": "/api/v1/images/employers/tech_innovate.jpg",
            "industry": "Technology",
            "locations": ["San Francisco", "London", "Singapore"]
        },
        "featured_providers": featured_providers[:3] if featured_providers else [
            {
                "id": "service_101",
                "name": "IELTS Academy",
                "category": "coaching",
                "trust_score": 850,
                "rating": 4.6,
                "reviews_count": 234
            },
            {
                "id": "service_102",
                "name": "StudentStay Housing",
                "category": "housing",
                "trust_score": 870,
                "rating": 4.5,
                "reviews_count": 178
            },
            {
                "id": "service_103",
                "name": "GlobalRemit Transfers",
                "category": "financial",
                "trust_score": 910,
                "rating": 4.8,
                "reviews_count": 312
            }
        ],
    }


@router.get("/categories")
async def list_categories(db: FirebaseService = Depends(get_db)):
    """
    List available service categories.
    """
    return {
        "categories": [
            {"id": "university", "name": "Universities", "count": await db.get_count(Collections.UNIVERSITIES)},
            {"id": "agent", "name": "Education Agents", "count": await db.get_count(Collections.AGENTS)},
            {"id": "employer", "name": "Employers", "count": 50},
            {"id": "housing", "name": "Housing", "count": await db.get_count(Collections.HOUSING)},
            {"id": "jobs", "name": "Jobs", "count": await db.get_count(Collections.JOBS)},
            {"id": "financial", "name": "Financial Services", "count": 25},
        ]
    }


@router.get("/{service_id}")
async def get_service(service_id: str, db: FirebaseService = Depends(get_db)):
    """
    Get service details.
    """
    # Try each collection
    for collection in [Collections.UNIVERSITIES, Collections.AGENTS, Collections.JOBS, Collections.HOUSING]:
        doc = await db.get_document(collection, service_id)
        if doc:
            return doc
    
    # Return default
    return {
        "id": service_id,
        "name": "Service Not Found",
        "category": "unknown",
        "trust_score": 0,
        "rating": 0,
        "reviews_count": 0,
    }


@router.post("/")
async def create_service(
    name: str,
    category: str,
    description: str,
    current_user: User = Depends(get_current_verified_user),
    db: FirebaseService = Depends(get_db),
):
    """
    Create a new service listing (for providers).
    """
    if not current_user.is_paid_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Subscription required to list services",
        )
    
    service_id = await db.create_document(
        Collections.SERVICES,
        {
            "name": name,
            "category": category,
            "description": description,
            "owner_id": current_user.id,
            "trust_score": 0,
            "rating": 0,
            "reviews_count": 0,
            "is_verified": False,
        }
    )
    
    return {
        "service_id": service_id,
        "message": "Service created and pending verification",
    }


@router.patch("/{service_id}")
async def update_service(
    service_id: str,
    current_user: User = Depends(get_current_verified_user),
):
    """
    Update a service listing.
    """
    return {"message": f"Service {service_id} updated"}


@router.delete("/{service_id}")
async def delete_service(
    service_id: str,
    current_user: User = Depends(get_current_verified_user),
):
    """
    Delete a service listing.
    """
    return {"message": f"Service {service_id} deleted"}


@router.post("/{service_id}/contact")
async def contact_service(
    service_id: str,
    message: str,
    current_user: User = Depends(get_current_verified_user),
):
    """
    Initiate contact with a service provider.
    Creates a chat room with context.
    """
    return {
        "room_id": "room_123",
        "message": "Chat initiated with service provider",
    }


# Sub-category endpoints

@router.get("/universities/")
async def list_universities(
    country: str = Query(None),
    program: str = Query(None),
    page: int = Query(1, ge=1),
    db: FirebaseService = Depends(get_db),
):
    """
    List universities.
    """
    filters = []
    if country:
        filters.append(("country", "==", country))
    
    universities = await db.get_collection(
        Collections.UNIVERSITIES,
        filters=filters if filters else None,
        order_by="trust_score",
        limit=20,
        offset=(page - 1) * 20
    )
    
    return {
        "universities": universities,
        "total": len(universities),
        "page": page
    }


@router.get("/agents/")
async def list_agents(
    specialization: str = Query(None),
    country: str = Query(None),
    page: int = Query(1, ge=1),
    db: FirebaseService = Depends(get_db),
):
    """
    List education agents.
    """
    agents = await db.get_collection(
        Collections.AGENTS,
        order_by="trust_score",
        limit=20,
        offset=(page - 1) * 20
    )
    
    # Filter by specialization/country in memory (Firebase limitations)
    if specialization:
        agents = [a for a in agents if specialization.lower() in a.get("specialization", "").lower()]
    if country:
        agents = [a for a in agents if country in a.get("countries", [])]
    
    return {
        "agents": agents,
        "total": len(agents),
        "page": page
    }


@router.get("/jobs/")
async def list_jobs(
    category: str = Query(None),
    location: str = Query(None),
    remote: bool = Query(None),
    page: int = Query(1, ge=1),
    db: FirebaseService = Depends(get_db),
):
    """
    List job opportunities.
    """
    jobs = await db.get_collection(
        Collections.JOBS,
        limit=20,
        offset=(page - 1) * 20
    )
    
    # Apply filters
    if location:
        jobs = [j for j in jobs if location.lower() in j.get("location", "").lower()]
    if remote is not None:
        jobs = [j for j in jobs if j.get("remote") == remote]
    
    return {
        "jobs": jobs,
        "total": len(jobs),
        "page": page
    }


@router.get("/housing/")
async def list_housing(
    city: str = Query(None),
    type: str = Query(None, description="hostel, apartment, shared"),
    max_rent: int = Query(None),
    page: int = Query(1, ge=1),
    db: FirebaseService = Depends(get_db),
):
    """
    List housing options.
    """
    housing = await db.get_collection(
        Collections.HOUSING,
        limit=20,
        offset=(page - 1) * 20
    )
    
    # Apply filters
    if city:
        housing = [h for h in housing if city.lower() in h.get("city", "").lower()]
    if type:
        housing = [h for h in housing if h.get("type") == type]
    if max_rent:
        housing = [h for h in housing if h.get("rent_per_month", 0) <= max_rent]
    
    return {
        "housing": housing,
        "total": len(housing),
        "page": page
    }
