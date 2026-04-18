import spacy
import re
from typing import Dict, List

nlp = spacy.load("en_core_web_sm")

def parse_resume(text: str) -> Dict:
    doc = nlp(text[:100000])
    skills = extract_skills(text)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phones = re.findall(r'(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', text)
    education = []
    for sent in doc.sents:
        if any(word in sent.text.lower() for word in ["bachelor", "master", "phd", "b.s.", "m.s.", "b.a."]):
            education.append(sent.text.strip())
    return {
        "skills": skills,
        "emails": emails,
        "phones": phones,
        "education": education[:3],
        "raw_text": text
    }

def extract_skills(text: str) -> List[str]:
    skill_keywords = [
        "python", "java", "javascript", "typescript", "react", "node", "django", "fastapi",
        "sql", "postgresql", "mongodb", "aws", "azure", "gcp", "docker", "kubernetes",
        "machine learning", "data science", "tensorflow", "pytorch", "nlp", "llm",
        "excel", "powerpoint", "leadership", "communication", "project management"
    ]
    found = []
    text_lower = text.lower()
    for skill in skill_keywords:
        if skill in text_lower:
            found.append(skill)
    return list(set(found))