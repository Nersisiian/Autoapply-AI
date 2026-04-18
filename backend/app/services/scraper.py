import random
from datetime import datetime, timedelta
from typing import List, Dict

# Simulated job feed (in production, replace with real APIs)
SAMPLE_JOBS = [
    {
        "external_id": "ind-001",
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "location": "Remote",
        "description": "We are looking for a Senior Python Developer with experience in FastAPI, Docker, and cloud platforms. Must have strong problem-solving skills and experience with microservices. You will be responsible for designing and implementing scalable backend services.",
        "url": "https://example.com/job/001",
        "source": "Indeed",
        "posted_date": datetime.now() - timedelta(days=2)
    },
    {
        "external_id": "li-002",
        "title": "Machine Learning Engineer",
        "company": "AI Innovations",
        "location": "San Francisco, CA",
        "description": "Join our ML team to build cutting-edge NLP models. Experience with PyTorch, Transformers, and production ML systems required. You'll work on large language models and deploy them to production.",
        "url": "https://example.com/job/002",
        "source": "LinkedIn",
        "posted_date": datetime.now() - timedelta(days=1)
    },
    {
        "external_id": "gh-003",
        "title": "Full Stack Developer",
        "company": "StartupX",
        "location": "New York, NY",
        "description": "Looking for a full-stack developer proficient in React, Node.js, and PostgreSQL. Experience with AWS is a plus. You'll be building features from frontend to backend in a fast-paced environment.",
        "url": "https://example.com/job/003",
        "source": "Glassdoor",
        "posted_date": datetime.now() - timedelta(days=3)
    },
    {
        "external_id": "ind-004",
        "title": "Data Scientist",
        "company": "DataInsights",
        "location": "Remote",
        "description": "Seeking a Data Scientist with strong Python and SQL skills. Experience with machine learning frameworks like scikit-learn and TensorFlow. You'll analyze large datasets and build predictive models.",
        "url": "https://example.com/job/004",
        "source": "Indeed",
        "posted_date": datetime.now() - timedelta(days=5)
    },
    {
        "external_id": "li-005",
        "title": "DevOps Engineer",
        "company": "CloudNative",
        "location": "Austin, TX",
        "description": "We need a DevOps Engineer experienced with Docker, Kubernetes, and CI/CD pipelines. Knowledge of AWS or GCP is essential. You'll help automate our infrastructure and deployment processes.",
        "url": "https://example.com/job/005",
        "source": "LinkedIn",
        "posted_date": datetime.now() - timedelta(days=1)
    },
]

def fetch_jobs(limit: int = 10) -> List[Dict]:
    """Simulate fetching jobs. In production, integrate with JSearch, SerpAPI, or scraping."""
    jobs = []
    for i in range(min(limit, len(SAMPLE_JOBS) * 2)):
        # Cycle through sample jobs and add slight variation
        base = SAMPLE_JOBS[i % len(SAMPLE_JOBS)].copy()
        base["external_id"] = f"{base['external_id']}-{random.randint(1000,9999)}"
        # Slight random variation in title
        if random.random() > 0.7:
            base["title"] = base["title"].replace("Senior", "Lead")
        jobs.append(base)
    return jobs