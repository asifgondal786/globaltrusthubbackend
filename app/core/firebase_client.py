"""
Firebase Database Client
Handles Firestore database operations for GlobalTrustHub.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from functools import lru_cache

from app.config import settings


class FirebaseClient:
    """Firebase Firestore client for database operations."""
    
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Firebase app and Firestore client."""
        try:
            # Check if already initialized
            firebase_admin.get_app()
        except ValueError:
            # Initialize Firebase
            cred_path = settings.FIREBASE_CREDENTIALS_PATH
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                # Initialize without credentials (uses GOOGLE_APPLICATION_CREDENTIALS env var)
                # Or use mock data mode
                print("⚠️ Firebase credentials not found, using mock data mode")
                self._db = None
                return
        
        self._db = firestore.client()
        print("✅ Firebase Firestore initialized")
    
    @property
    def db(self):
        return self._db
    
    @property
    def is_connected(self) -> bool:
        return self._db is not None


# Collection names
class Collections:
    USERS = "users"
    SERVICES = "services"
    UNIVERSITIES = "universities"
    AGENTS = "agents"
    EMPLOYERS = "employers"
    JOBS = "jobs"
    HOUSING = "housing"
    REVIEWS = "reviews"
    NEWS = "news"
    JOURNEYS = "journeys"
    CHAT_ROOMS = "chat_rooms"
    MESSAGES = "messages"
    TRUST_SCORES = "trust_scores"
    ML_PREDICTIONS = "ml_predictions"


class FirebaseService:
    """Service layer for Firebase operations."""
    
    def __init__(self):
        self.client = FirebaseClient()
    
    # ---------- Generic CRUD Operations ----------
    
    async def get_document(self, collection: str, doc_id: str) -> Optional[Dict]:
        """Get a single document by ID."""
        if not self.client.is_connected:
            return self._get_mock_document(collection, doc_id)
        
        doc_ref = self.client.db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None
    
    async def get_collection(
        self, 
        collection: str, 
        filters: List[tuple] = None,
        order_by: str = None,
        order_direction: str = "DESCENDING",
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict]:
        """Get documents from a collection with optional filters."""
        if not self.client.is_connected:
            return self._get_mock_collection(collection, limit)
        
        query = self.client.db.collection(collection)
        
        # Apply filters
        if filters:
            for field, op, value in filters:
                query = query.where(field, op, value)
        
        # Apply ordering
        if order_by:
            direction = firestore.Query.DESCENDING if order_direction == "DESCENDING" else firestore.Query.ASCENDING
            query = query.order_by(order_by, direction=direction)
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        docs = query.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    
    async def create_document(self, collection: str, data: Dict, doc_id: str = None) -> str:
        """Create a new document."""
        if not self.client.is_connected:
            return "mock_id_123"
        
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        
        if doc_id:
            self.client.db.collection(collection).document(doc_id).set(data)
            return doc_id
        else:
            doc_ref = self.client.db.collection(collection).add(data)
            return doc_ref[1].id
    
    async def update_document(self, collection: str, doc_id: str, data: Dict) -> bool:
        """Update a document."""
        if not self.client.is_connected:
            return True
        
        data["updated_at"] = datetime.utcnow()
        self.client.db.collection(collection).document(doc_id).update(data)
        return True
    
    async def delete_document(self, collection: str, doc_id: str) -> bool:
        """Delete a document."""
        if not self.client.is_connected:
            return True
        
        self.client.db.collection(collection).document(doc_id).delete()
        return True
    
    async def get_count(self, collection: str, filters: List[tuple] = None) -> int:
        """Get document count in a collection."""
        if not self.client.is_connected:
            return 100  # Mock count
        
        query = self.client.db.collection(collection)
        if filters:
            for field, op, value in filters:
                query = query.where(field, op, value)
        
        # Note: Firestore doesn't have a direct count, using aggregation
        return len(list(query.stream()))
    
    # ---------- Mock Data Methods ----------
    
    def _get_mock_document(self, collection: str, doc_id: str) -> Optional[Dict]:
        """Return mock document for development."""
        mock_data = self._get_mock_data(collection)
        for item in mock_data:
            if item.get("id") == doc_id:
                return item
        return mock_data[0] if mock_data else None
    
    def _get_mock_collection(self, collection: str, limit: int = 20) -> List[Dict]:
        """Return mock collection for development."""
        return self._get_mock_data(collection)[:limit]
    
    def _get_mock_data(self, collection: str) -> List[Dict]:
        """Get mock data based on collection name."""
        if collection == Collections.UNIVERSITIES:
            return [
                {"id": "uni_001", "name": "Harvard University", "country": "USA", "trust_score": 980, "rating": 4.9, "reviews_count": 324, "programs": ["Business", "Law", "Medicine"], "is_verified": True},
                {"id": "uni_002", "name": "University of Oxford", "country": "UK", "trust_score": 975, "rating": 4.9, "reviews_count": 298, "programs": ["Arts", "Sciences", "Law"], "is_verified": True},
                {"id": "uni_003", "name": "University of Toronto", "country": "Canada", "trust_score": 950, "rating": 4.8, "reviews_count": 256, "programs": ["Engineering", "Business", "Medicine"], "is_verified": True},
                {"id": "uni_004", "name": "University of Melbourne", "country": "Australia", "trust_score": 945, "rating": 4.7, "reviews_count": 234, "programs": ["Arts", "Engineering", "Business"], "is_verified": True},
                {"id": "uni_005", "name": "MIT", "country": "USA", "trust_score": 985, "rating": 4.9, "reviews_count": 312, "programs": ["Engineering", "Technology", "Sciences"], "is_verified": True},
            ]
        elif collection == Collections.AGENTS:
            return [
                {"id": "agent_001", "name": "Ali Travel Consultants", "specialization": "Study Abroad", "trust_score": 920, "rating": 4.8, "reviews_count": 156, "countries": ["UK", "Canada", "Australia"], "is_verified": True},
                {"id": "agent_002", "name": "Global Visa Services", "specialization": "Work Visa", "trust_score": 890, "rating": 4.6, "reviews_count": 134, "countries": ["USA", "UK", "Germany"], "is_verified": True},
                {"id": "agent_003", "name": "EduConnect Pro", "specialization": "University Admissions", "trust_score": 910, "rating": 4.7, "reviews_count": 178, "countries": ["Canada", "Australia", "NZ"], "is_verified": True},
            ]
        elif collection == Collections.JOBS:
            return [
                {"id": "job_001", "title": "Software Engineer", "company": "Tech Innovate Inc.", "location": "San Francisco, USA", "salary_range": "$120k-$180k", "type": "Full-time", "remote": True, "is_verified": True},
                {"id": "job_002", "title": "Data Scientist", "company": "AI Research Lab", "location": "London, UK", "salary_range": "£60k-£90k", "type": "Full-time", "remote": True, "is_verified": True},
                {"id": "job_003", "title": "Product Manager", "company": "StartupHub", "location": "Toronto, Canada", "salary_range": "CAD $90k-$130k", "type": "Full-time", "remote": False, "is_verified": True},
                {"id": "job_004", "title": "UX Designer", "company": "Design Studio", "location": "Berlin, Germany", "salary_range": "€55k-€75k", "type": "Full-time", "remote": True, "is_verified": True},
            ]
        elif collection == Collections.NEWS:
            return [
                {"id": "news_001", "title": "UK Updates Work Visa Rules", "source": "UK Home Office", "category": "immigration", "published_at": datetime.utcnow(), "summary": "New changes to UK work visa requirements..."},
                {"id": "news_002", "title": "Canada Increases Student Work Hours", "source": "Immigration Canada", "category": "education", "published_at": datetime.utcnow(), "summary": "International students can now work more hours..."},
                {"id": "news_003", "title": "Australia Eases Travel Restrictions", "source": "AU Border Force", "category": "travel", "published_at": datetime.utcnow(), "summary": "New travel policies announced..."},
            ]
        elif collection == Collections.HOUSING:
            return [
                {"id": "housing_001", "name": "StudentStay London", "type": "hostel", "city": "London", "rent_per_month": 800, "rating": 4.5, "is_verified": True},
                {"id": "housing_002", "name": "Campus Living Toronto", "type": "apartment", "city": "Toronto", "rent_per_month": 1200, "rating": 4.6, "is_verified": True},
            ]
        else:
            return []


@lru_cache()
def get_firebase_service() -> FirebaseService:
    """Get cached Firebase service instance."""
    return FirebaseService()


# Dependency for FastAPI
def get_db() -> FirebaseService:
    """Dependency to get Firebase service."""
    return get_firebase_service()
