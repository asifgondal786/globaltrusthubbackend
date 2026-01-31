"""
Journey API Router
User journey progress tracking endpoints.
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def list_journeys():
    """
    List available journey templates.
    """
    return {
        "journeys": [
            {
                "id": "study_abroad",
                "name": "Study Abroad Journey",
                "description": "Complete guide for international education",
                "milestones_count": 5,
            },
            {
                "id": "work_abroad",
                "name": "Work Abroad Journey",
                "description": "Steps to secure international employment",
                "milestones_count": 6,
            },
            {
                "id": "immigration",
                "name": "Immigration Journey",
                "description": "Pathway to permanent residency",
                "milestones_count": 7,
            },
        ]
    }


@router.get("/my-progress")
async def get_my_journey_progress(
    # current_user: User = Depends(get_current_active_user),
):
    """
    Get current user's journey progress.
    Returns sample data for demonstration.
    """
    return {
        "journey_id": "study_abroad",
        "journey_name": "Study Abroad - Canada",
        "started_at": "2024-01-15T10:00:00Z",
        "current_milestone": 3,
        "milestones": [
            {
                "id": 1,
                "name": "Application",
                "description": "Submit university applications",
                "status": "completed",
                "completed_at": "2024-02-01T14:30:00Z",
                "icon": "description",
            },
            {
                "id": 2,
                "name": "Visa Approved",
                "description": "Obtain student visa",
                "status": "completed",
                "completed_at": "2024-03-15T09:00:00Z",
                "icon": "verified",
            },
            {
                "id": 3,
                "name": "Travel",
                "description": "Book flights and travel",
                "status": "completed",
                "completed_at": "2024-04-20T16:00:00Z",
                "icon": "flight",
            },
            {
                "id": 4,
                "name": "Accommodation",
                "description": "Secure housing",
                "status": "in_progress",
                "completed_at": None,
                "icon": "home",
            },
            {
                "id": 5,
                "name": "Job Secured",
                "description": "Find part-time employment",
                "status": "pending",
                "completed_at": None,
                "icon": "work",
            },
        ],
        "progress_percentage": 60,
        "next_action": {
            "title": "Complete accommodation booking",
            "description": "Finalize your student housing arrangement",
            "action_url": "/services/housing",
        },
    }


@router.post("/milestones/{milestone_id}/complete")
async def complete_milestone(
    milestone_id: int,
    # current_user: User = Depends(get_current_active_user),
):
    """
    Mark a milestone as complete.
    """
    return {
        "message": f"Milestone {milestone_id} marked as complete",
        "milestone_id": milestone_id,
        "completed_at": datetime.now().isoformat(),
    }


@router.get("/templates/{template_id}")
async def get_journey_template(template_id: str):
    """
    Get journey template details.
    """
    templates = {
        "study_abroad": {
            "id": "study_abroad",
            "name": "Study Abroad Journey",
            "description": "Complete guide for international education",
            "milestones": [
                {"id": 1, "name": "Application", "description": "Submit applications"},
                {"id": 2, "name": "Visa Approved", "description": "Get student visa"},
                {"id": 3, "name": "Travel", "description": "Arrange travel"},
                {"id": 4, "name": "Accommodation", "description": "Find housing"},
                {"id": 5, "name": "Job Secured", "description": "Get part-time job"},
            ],
        },
    }
    
    return templates.get(template_id, {"error": "Template not found"})
