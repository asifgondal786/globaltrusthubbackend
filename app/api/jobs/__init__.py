from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(tags=["jobs"])

# Employer model
class Employer(BaseModel):
    id: str
    name: str
    logo_url: Optional[str] = None
    industry: str
    company_size: str
    location: str
    website: Optional[str] = None
    verified: bool = False
    rating: Optional[float] = None
    review_count: int = 0

# Job model
class Job(BaseModel):
    id: str
    title: str
    employer: Employer
    location: str
    country: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    salary_period: str = "yearly"  # yearly, monthly, hourly
    job_type: str  # full-time, part-time, contract, internship
    remote: bool = False
    category: str
    experience_level: str  # entry, mid, senior, executive
    description: str
    requirements: List[str]
    benefits: List[str]
    posted_date: str
    application_deadline: Optional[str] = None
    applicants: int = 0
    source: str  # linkedin, indeed, company, etc.
    apply_url: str
    is_sponsored: bool = False

class JobsResponse(BaseModel):
    jobs: List[Job]
    total: int
    page: int
    page_size: int

# Sample employers
EMPLOYERS = {
    "google": Employer(
        id="emp_001",
        name="Google",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
        industry="Technology",
        company_size="10,000+ employees",
        location="Mountain View, CA, USA",
        website="https://careers.google.com",
        verified=True,
        rating=4.5,
        review_count=12500
    ),
    "microsoft": Employer(
        id="emp_002",
        name="Microsoft",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg",
        industry="Technology",
        company_size="10,000+ employees",
        location="Redmond, WA, USA",
        website="https://careers.microsoft.com",
        verified=True,
        rating=4.3,
        review_count=9800
    ),
    "amazon": Employer(
        id="emp_003",
        name="Amazon",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        industry="E-commerce / Technology",
        company_size="10,000+ employees",
        location="Seattle, WA, USA",
        website="https://amazon.jobs",
        verified=True,
        rating=4.0,
        review_count=15600
    ),
    "deloitte": Employer(
        id="emp_004",
        name="Deloitte",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/5/56/Deloitte.svg",
        industry="Consulting",
        company_size="10,000+ employees",
        location="London, UK",
        website="https://careers.deloitte.com",
        verified=True,
        rating=4.1,
        review_count=8700
    ),
    "hsbc": Employer(
        id="emp_005",
        name="HSBC",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/a/aa/HSBC_logo_%282018%29.svg",
        industry="Banking & Finance",
        company_size="10,000+ employees",
        location="London, UK",
        website="https://careers.hsbc.com",
        verified=True,
        rating=3.9,
        review_count=5400
    ),
    "nhs": Employer(
        id="emp_006",
        name="NHS (National Health Service)",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/d/d3/NHS_logo.svg",
        industry="Healthcare",
        company_size="10,000+ employees",
        location="United Kingdom",
        website="https://jobs.nhs.uk",
        verified=True,
        rating=4.2,
        review_count=7800
    ),
    "emirates": Employer(
        id="emp_007",
        name="Emirates Group",
        logo_url="https://upload.wikimedia.org/wikipedia/commons/d/d0/Emirates_logo.svg",
        industry="Aviation",
        company_size="10,000+ employees",
        location="Dubai, UAE",
        website="https://careers.emirates.com",
        verified=True,
        rating=4.4,
        review_count=3200
    ),
    "shopify": Employer(
        id="emp_008",
        name="Shopify",
        industry="E-commerce / Technology",
        company_size="5,000-10,000 employees",
        location="Ottawa, Canada",
        website="https://careers.shopify.com",
        verified=True,
        rating=4.6,
        review_count=2100
    ),
    "canva": Employer(
        id="emp_009",
        name="Canva",
        industry="Technology / Design",
        company_size="1,000-5,000 employees",
        location="Sydney, Australia",
        website="https://canva.com/careers",
        verified=True,
        rating=4.7,
        review_count=1500
    ),
    "siemens": Employer(
        id="emp_010",
        name="Siemens",
        industry="Manufacturing / Technology",
        company_size="10,000+ employees",
        location="Munich, Germany",
        website="https://jobs.siemens.com",
        verified=True,
        rating=4.2,
        review_count=6300
    ),
}

# Sample Jobs Database
JOBS: List[Job] = [
    Job(
        id="job_001",
        title="Senior Software Engineer",
        employer=EMPLOYERS["google"],
        location="Mountain View, CA",
        country="USA",
        salary_min=180000,
        salary_max=250000,
        salary_currency="USD",
        salary_period="yearly",
        job_type="full-time",
        remote=True,
        category="Technology",
        experience_level="senior",
        description="Join Google's Cloud Platform team to build next-generation infrastructure services. You'll work on distributed systems that power millions of users worldwide.",
        requirements=["5+ years of software development", "Experience with distributed systems", "Proficiency in Go, Java, or Python", "Strong problem-solving skills"],
        benefits=["Health insurance", "401k matching", "Unlimited PTO", "Stock options", "Free meals"],
        posted_date="2026-01-25",
        applicants=245,
        source="linkedin",
        apply_url="https://careers.google.com/jobs/results/123",
        is_sponsored=True
    ),
    Job(
        id="job_002",
        title="Product Manager",
        employer=EMPLOYERS["microsoft"],
        location="Seattle, WA",
        country="USA",
        salary_min=140000,
        salary_max=200000,
        salary_currency="USD",
        salary_period="yearly",
        job_type="full-time",
        remote=False,
        category="Product",
        experience_level="mid",
        description="Lead product strategy for Microsoft Teams. Define roadmap, work with engineering teams, and drive product launches that impact millions of users.",
        requirements=["3+ years product management experience", "Technical background preferred", "Excellent communication skills", "Experience with Agile methodologies"],
        benefits=["Health insurance", "Annual bonus", "Stock options", "Parental leave"],
        posted_date="2026-01-24",
        applicants=178,
        source="linkedin",
        apply_url="https://careers.microsoft.com/jobs/12345"
    ),
    Job(
        id="job_003",
        title="Data Scientist",
        employer=EMPLOYERS["amazon"],
        location="Vancouver, BC",
        country="Canada",
        salary_min=120000,
        salary_max=180000,
        salary_currency="CAD",
        salary_period="yearly",
        job_type="full-time",
        remote=True,
        category="Data Science",
        experience_level="mid",
        description="Analyze large datasets to drive business decisions. Build ML models to improve customer experience and optimize operations.",
        requirements=["MS in Statistics, CS, or related field", "Experience with Python, SQL", "Knowledge of ML frameworks", "Strong analytical skills"],
        benefits=["Relocation assistance", "Health insurance", "Stock options"],
        posted_date="2026-01-23",
        applicants=312,
        source="indeed",
        apply_url="https://amazon.jobs/en/jobs/12345"
    ),
    Job(
        id="job_004",
        title="Management Consultant",
        employer=EMPLOYERS["deloitte"],
        location="London",
        country="UK",
        salary_min=55000,
        salary_max=85000,
        salary_currency="GBP",
        salary_period="yearly",
        job_type="full-time",
        remote=False,
        category="Consulting",
        experience_level="entry",
        description="Join our Strategy & Operations practice. Work with Fortune 500 clients on transformational projects across industries.",
        requirements=["Bachelor's degree required", "Strong analytical skills", "Excellent presentation skills", "Willingness to travel"],
        benefits=["Performance bonus", "Private healthcare", "Pension scheme", "Training budget"],
        posted_date="2026-01-26",
        applicants=89,
        source="company",
        apply_url="https://careers.deloitte.com/jobs/123",
        is_sponsored=True
    ),
    Job(
        id="job_005",
        title="Financial Analyst",
        employer=EMPLOYERS["hsbc"],
        location="Canary Wharf, London",
        country="UK",
        salary_min=45000,
        salary_max=65000,
        salary_currency="GBP",
        salary_period="yearly",
        job_type="full-time",
        remote=False,
        category="Finance",
        experience_level="entry",
        description="Support investment banking division with financial modeling, valuation analysis, and client presentations.",
        requirements=["Degree in Finance or Accounting", "Excel proficiency", "CFA Level 1 preferred", "Attention to detail"],
        benefits=["Bonus scheme", "Pension", "Healthcare", "Professional development"],
        posted_date="2026-01-22",
        applicants=156,
        source="linkedin",
        apply_url="https://careers.hsbc.com/jobs/123"
    ),
    Job(
        id="job_006",
        title="Registered Nurse",
        employer=EMPLOYERS["nhs"],
        location="Manchester",
        country="UK",
        salary_min=28000,
        salary_max=38000,
        salary_currency="GBP",
        salary_period="yearly",
        job_type="full-time",
        remote=False,
        category="Healthcare",
        experience_level="entry",
        description="Join our acute care ward. Provide compassionate patient care, administer medications, and work with multidisciplinary teams.",
        requirements=["NMC registration", "BSc Nursing", "Strong communication skills", "Ability to work shifts"],
        benefits=["NHS pension", "27 days leave", "Training opportunities", "Visa sponsorship available"],
        posted_date="2026-01-27",
        applicants=45,
        source="company",
        apply_url="https://jobs.nhs.uk/job/123"
    ),
    Job(
        id="job_007",
        title="Cabin Crew",
        employer=EMPLOYERS["emirates"],
        location="Dubai",
        country="UAE",
        salary_min=10000,
        salary_max=15000,
        salary_currency="AED",
        salary_period="monthly",
        job_type="full-time",
        remote=False,
        category="Aviation",
        experience_level="entry",
        description="Deliver world-class service to passengers. Ensure safety and comfort on international flights.",
        requirements=["High school diploma", "Fluent English", "Minimum height 160cm", "No visible tattoos", "Hospitality experience preferred"],
        benefits=["Tax-free salary", "Free accommodation", "Travel benefits", "Medical insurance", "Annual leave tickets"],
        posted_date="2026-01-20",
        applicants=890,
        source="company",
        apply_url="https://careers.emirates.com/cabin-crew",
        is_sponsored=True
    ),
    Job(
        id="job_008",
        title="Full Stack Developer",
        employer=EMPLOYERS["shopify"],
        location="Toronto, ON",
        country="Canada",
        salary_min=100000,
        salary_max=150000,
        salary_currency="CAD",
        salary_period="yearly",
        job_type="full-time",
        remote=True,
        category="Technology",
        experience_level="mid",
        description="Build merchant-facing features using Ruby on Rails and React. Impact millions of businesses worldwide.",
        requirements=["3+ years full stack experience", "Ruby on Rails proficiency", "React/TypeScript experience", "E-commerce knowledge a plus"],
        benefits=["Stock options", "Flexible work", "Health benefits", "Home office budget"],
        posted_date="2026-01-26",
        applicants=234,
        source="linkedin",
        apply_url="https://careers.shopify.com/jobs/123"
    ),
    Job(
        id="job_009",
        title="UX Designer",
        employer=EMPLOYERS["canva"],
        location="Sydney",
        country="Australia",
        salary_min=95000,
        salary_max=130000,
        salary_currency="AUD",
        salary_period="yearly",
        job_type="full-time",
        remote=True,
        category="Design",
        experience_level="mid",
        description="Design intuitive experiences for our design platform used by 100+ million users. Conduct user research and create prototypes.",
        requirements=["3+ years UX design experience", "Figma proficiency", "Portfolio required", "User research experience"],
        benefits=["Equity package", "Wellness budget", "Learning allowance", "Flexible hours"],
        posted_date="2026-01-25",
        applicants=167,
        source="linkedin",
        apply_url="https://canva.com/careers/job/123"
    ),
    Job(
        id="job_010",
        title="Mechanical Engineer",
        employer=EMPLOYERS["siemens"],
        location="Munich",
        country="Germany",
        salary_min=55000,
        salary_max=75000,
        salary_currency="EUR",
        salary_period="yearly",
        job_type="full-time",
        remote=False,
        category="Engineering",
        experience_level="mid",
        description="Design and develop industrial automation systems. Work on cutting-edge robotics and manufacturing solutions.",
        requirements=["Degree in Mechanical Engineering", "CAD software proficiency", "German language B2 level", "Industry experience preferred"],
        benefits=["German work permit sponsorship", "Relocation support", "Pension scheme", "30 days leave"],
        posted_date="2026-01-24",
        applicants=78,
        source="indeed",
        apply_url="https://jobs.siemens.com/job/123"
    ),
    Job(
        id="job_011",
        title="Marketing Coordinator",
        employer=EMPLOYERS["canva"],
        location="Remote",
        country="Australia",
        salary_min=70000,
        salary_max=90000,
        salary_currency="AUD",
        salary_period="yearly",
        job_type="full-time",
        remote=True,
        category="Marketing",
        experience_level="entry",
        description="Support global marketing campaigns. Manage social media, coordinate events, and create content.",
        requirements=["Bachelor's in Marketing", "Social media savvy", "Excellent writing skills", "Creative mindset"],
        benefits=["Equity", "Learning budget", "Remote work", "Team offsites"],
        posted_date="2026-01-27",
        applicants=203,
        source="company",
        apply_url="https://canva.com/careers/job/456"
    ),
    Job(
        id="job_012",
        title="DevOps Engineer",
        employer=EMPLOYERS["microsoft"],
        location="Dublin",
        country="Ireland",
        salary_min=80000,
        salary_max=120000,
        salary_currency="EUR",
        salary_period="yearly",
        job_type="full-time",
        remote=True,
        category="Technology",
        experience_level="senior",
        description="Build and maintain CI/CD pipelines for Azure services. Ensure high availability and security of cloud infrastructure.",
        requirements=["5+ years DevOps experience", "Azure/AWS expertise", "Kubernetes proficiency", "Infrastructure as Code"],
        benefits=["Stock options", "Annual bonus", "Health insurance", "Relocation support"],
        posted_date="2026-01-23",
        applicants=134,
        source="linkedin",
        apply_url="https://careers.microsoft.com/jobs/67890"
    ),
]

@router.get("", response_model=JobsResponse)
async def get_jobs(
    category: Optional[str] = Query(None, description="Filter by category"),
    country: Optional[str] = Query(None, description="Filter by country"),
    remote: Optional[bool] = Query(None, description="Filter remote jobs"),
    experience_level: Optional[str] = Query(None, description="Filter by experience level"),
    search: Optional[str] = Query(None, description="Search in title or description"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Jobs per page")
):
    """Get list of jobs with optional filters"""
    filtered_jobs = JOBS.copy()
    
    # Apply filters
    if category:
        filtered_jobs = [j for j in filtered_jobs if j.category.lower() == category.lower()]
    
    if country:
        filtered_jobs = [j for j in filtered_jobs if j.country.lower() == country.lower()]
    
    if remote is not None:
        filtered_jobs = [j for j in filtered_jobs if j.remote == remote]
    
    if experience_level:
        filtered_jobs = [j for j in filtered_jobs if j.experience_level.lower() == experience_level.lower()]
    
    if search:
        search_lower = search.lower()
        filtered_jobs = [j for j in filtered_jobs if search_lower in j.title.lower() or search_lower in j.description.lower()]
    
    # Pagination
    total = len(filtered_jobs)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_jobs = filtered_jobs[start_idx:end_idx]
    
    return JobsResponse(
        jobs=paginated_jobs,
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/categories")
async def get_job_categories():
    """Get list of available job categories"""
    categories = list(set(job.category for job in JOBS))
    return {"categories": sorted(categories)}

@router.get("/countries")
async def get_countries():
    """Get list of countries with available jobs"""
    countries = list(set(job.country for job in JOBS))
    return {"countries": sorted(countries)}

@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """Get detailed job information"""
    for job in JOBS:
        if job.id == job_id:
            return job
    raise HTTPException(status_code=404, detail="Job not found")
