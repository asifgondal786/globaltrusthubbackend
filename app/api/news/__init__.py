"""
News API Router
Latest news and updates endpoints with comprehensive sample data.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Query

router = APIRouter()

# Comprehensive sample news data
SAMPLE_NEWS = [
    # University News
    {
        "id": "news_001",
        "title": "Harvard Announces New AI Research Center",
        "summary": "Harvard University opens state-of-the-art AI research facility with $500M investment.",
        "category": "university",
        "country": "USA",
        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
        "time_ago": "1h ago",
        "image": None,
        "url": "/news/harvard-ai-center"
    },
    {
        "id": "news_002",
        "title": "Oxford University Expands International Scholarships",
        "summary": "100 new fully-funded scholarships available for students from developing countries.",
        "category": "university",
        "country": "UK",
        "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
        "time_ago": "3h ago",
        "image": None,
        "url": "/news/oxford-scholarships"
    },
    {
        "id": "news_003",
        "title": "University of Melbourne Tops Australian Rankings",
        "summary": "Melbourne rises to #1 in Australia for engineering and computer science programs.",
        "category": "university",
        "country": "Australia",
        "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(),
        "time_ago": "5h ago",
        "image": None,
        "url": "/news/melbourne-rankings"
    },
    
    # Visa Policies
    {
        "id": "news_004",
        "title": "UK Updates Work Visa Rules",
        "summary": "New changes to graduate work visa allow extended stay for international students.",
        "category": "visa",
        "country": "UK",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "time_ago": "2h ago",
        "image": None,
        "url": "/news/uk-work-visa-updates"
    },
    {
        "id": "news_005",
        "title": "Germany Introduces Fast-Track Student Visa",
        "summary": "New express processing for qualified international students - 2 weeks approval.",
        "category": "visa",
        "country": "Germany",
        "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(),
        "time_ago": "8h ago",
        "image": None,
        "url": "/news/germany-fast-track-visa"
    },
    {
        "id": "news_006",
        "title": "Canada Simplifies PR Application for Students",
        "summary": "Post-graduation work permit holders can now apply for PR within 6 months.",
        "category": "visa",
        "country": "Canada",
        "timestamp": (datetime.now() - timedelta(hours=10)).isoformat(),
        "time_ago": "10h ago",
        "image": None,
        "url": "/news/canada-pr-students"
    },
    
    # Education Trends
    {
        "id": "news_007",
        "title": "Remote Learning Becomes Standard in Top Universities",
        "summary": "Major universities adopt hybrid learning models permanently post-pandemic.",
        "category": "education",
        "country": "Global",
        "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
        "time_ago": "4h ago",
        "image": None,
        "url": "/news/remote-learning-trend"
    },
    {
        "id": "news_008",
        "title": "STEM Programs See Record Enrollment",
        "summary": "Engineering and tech courses attract 40% more international students this year.",
        "category": "education",
        "country": "Global",
        "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
        "time_ago": "6h ago",
        "image": None,
        "url": "/news/stem-enrollment"
    },
    {
        "id": "news_009",
        "title": "Canada Increases Student Work Hours",
        "summary": "International students can now work up to 24 hours per week during study periods.",
        "category": "education",
        "country": "Canada",
        "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
        "time_ago": "4h ago",
        "image": None,
        "url": "/news/canada-student-work-hours"
    },
    
    # Accommodation
    {
        "id": "news_010",
        "title": "London Student Housing Crisis Eases",
        "summary": "New affordable student accommodations open near major universities in London.",
        "category": "accommodation",
        "country": "UK",
        "timestamp": (datetime.now() - timedelta(hours=7)).isoformat(),
        "time_ago": "7h ago",
        "image": None,
        "url": "/news/london-student-housing"
    },
    {
        "id": "news_011",
        "title": "Sydney Launches Student Housing Portal",
        "summary": "Official platform helps international students find verified accommodation.",
        "category": "accommodation",
        "country": "Australia",
        "timestamp": (datetime.now() - timedelta(hours=12)).isoformat(),
        "time_ago": "12h ago",
        "image": None,
        "url": "/news/sydney-housing-portal"
    },
    {
        "id": "news_012",
        "title": "Berlin Rent Control Benefits Students",
        "summary": "New rent cap legislation makes German capital more affordable for students.",
        "category": "accommodation",
        "country": "Germany",
        "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
        "time_ago": "1d ago",
        "image": None,
        "url": "/news/berlin-rent-control"
    },
    
    # Employment
    {
        "id": "news_013",
        "title": "US Tech Companies Increase H1B Sponsorship",
        "summary": "Major tech firms announce plans to sponsor 50% more international talent.",
        "category": "employment",
        "country": "USA",
        "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
        "time_ago": "3h ago",
        "image": None,
        "url": "/news/us-h1b-sponsorship"
    },
    {
        "id": "news_014",
        "title": "Germany Fast-Tracks Skilled Worker Visas",
        "summary": "IT professionals can now get work permits within 4 weeks.",
        "category": "employment",
        "country": "Germany",
        "timestamp": (datetime.now() - timedelta(hours=9)).isoformat(),
        "time_ago": "9h ago",
        "image": None,
        "url": "/news/germany-skilled-workers"
    },
    {
        "id": "news_015",
        "title": "Australia Expands Skilled Migration List",
        "summary": "Healthcare and engineering professionals added to priority migration list.",
        "category": "employment",
        "country": "Australia",
        "timestamp": (datetime.now() - timedelta(hours=11)).isoformat(),
        "time_ago": "11h ago",
        "image": None,
        "url": "/news/australia-skilled-migration"
    },
    {
        "id": "news_016",
        "title": "Remote Work Opportunities Surge in Europe",
        "summary": "Major companies offering remote positions with visa sponsorship.",
        "category": "employment",
        "country": "Europe",
        "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
        "time_ago": "1d ago",
        "image": None,
        "url": "/news/europe-remote-work"
    },
    
    # Travel / Countries
    {
        "id": "news_017",
        "title": "Australia Eases Travel Restrictions",
        "summary": "Simplified visa processing for skilled workers and students from partner countries.",
        "category": "travel",
        "country": "Australia",
        "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
        "time_ago": "6h ago",
        "image": None,
        "url": "/news/australia-travel-restrictions"
    },
    {
        "id": "news_018",
        "title": "New Zealand Reopens Borders Fully",
        "summary": "All visa categories now being processed with no COVID restrictions.",
        "category": "travel",
        "country": "New Zealand",
        "timestamp": (datetime.now() - timedelta(hours=14)).isoformat(),
        "time_ago": "14h ago",
        "image": None,
        "url": "/news/nz-borders-open"
    },
    {
        "id": "news_019",
        "title": "Japan Welcomes International Students Again",
        "summary": "Japanese universities see surge in applications after border reopening.",
        "category": "travel",
        "country": "Japan",
        "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
        "time_ago": "1d ago",
        "image": None,
        "url": "/news/japan-students"
    },
]


@router.get("/")
async def list_news(
    category: str = Query(None, description="university, education, visa, accommodation, employment, travel"),
    country: str = Query(None),
    limit: int = Query(10, ge=1, le=50),
):
    """
    List latest news and updates.
    
    Categories:
    - university: International university news, admissions, rankings
    - education: Education trends, study abroad tips
    - visa: Visa policies, immigration updates
    - accommodation: Housing, hostels, landlord news
    - employment: Job market, employer updates, sponsorship
    - travel: Country travel policies, restrictions
    """
    news_items = SAMPLE_NEWS.copy()
    
    # Filter by category if provided
    if category:
        news_items = [n for n in news_items if n["category"] == category]
    
    # Filter by country if provided
    if country:
        news_items = [n for n in news_items if n["country"].lower() == country.lower()]
    
    return {
        "news": news_items[:limit],
        "total": len(news_items),
        "categories": ["university", "education", "visa", "accommodation", "employment", "travel"],
    }


@router.get("/categories")
async def list_categories():
    """
    List all available news categories.
    """
    return {
        "categories": [
            {"id": "university", "name": "University News", "icon": "school"},
            {"id": "education", "name": "Education Trends", "icon": "trending_up"},
            {"id": "visa", "name": "Visa Policies", "icon": "badge"},
            {"id": "accommodation", "name": "Accommodation", "icon": "home"},
            {"id": "employment", "name": "Employment", "icon": "work"},
            {"id": "travel", "name": "Travel Updates", "icon": "flight"},
        ]
    }


@router.get("/{news_id}")
async def get_news_detail(news_id: str):
    """
    Get news article details.
    """
    # Find the news item
    news_item = next((n for n in SAMPLE_NEWS if n["id"] == news_id), None)
    
    if news_item:
        return {
            **news_item,
            "content": f"Full article content for: {news_item['title']}. This is detailed information about the news story...",
            "author": "GlobalTrustHub News Team",
            "related_news": [n for n in SAMPLE_NEWS if n["category"] == news_item["category"] and n["id"] != news_id][:3],
        }
    
    return {
        "id": news_id,
        "title": "News Article Not Found",
        "content": "The requested news article could not be found.",
        "category": "general",
        "country": "Global",
        "timestamp": datetime.now().isoformat(),
        "author": "GlobalTrustHub News Team",
        "related_news": [],
    }
