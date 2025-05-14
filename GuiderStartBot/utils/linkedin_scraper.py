# utils/linkedin_scraper.py

import random

def scrape_linkedin_profile(name, organization, linkedin_url):
    """
    Simulates scraping public info from LinkedIn.
    """
    # Simulated titles and skills
    fake_titles = [
        "Senior AI Scientist", "ML Engineer", "Data Scientist", 
        "AI Researcher", "Solution Architect"
    ]

    fake_skills = [
        ["AI", "Machine Learning", "Python"],
        ["GenAI", "Prompt Engineering", "LangChain"],
        ["Data Science", "TensorFlow", "Pandas"],
        ["Cloud", "Docker", "APIs"],
        ["Healthcare AI", "Edge AI", "LLMs"]
    ]

    return {
        "name": name,
        "organization": organization,
        "linkedin": linkedin_url,
        "title": random.choice(fake_titles),
        "skills": random.choice(fake_skills)
    }
