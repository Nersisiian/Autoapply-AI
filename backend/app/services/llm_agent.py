import json
import requests
from openai import OpenAI
from ..config import settings
from ..schemas import CoverLetterResponse

def generate_cover_letter(job_description: str, resume_text: str) -> CoverLetterResponse:
    prompt = f"""
You are an expert career coach and professional writer. Your task is to create a personalized cover letter based on the job description and the candidate's resume.

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Generate a response in valid JSON format with the following keys:
- "cover_letter": A professional cover letter (string)
- "explanation": A brief explanation of why the candidate is a strong match (string)
- "suggestions": A list of 2-3 actionable suggestions to improve the candidate's profile for this role (array of strings)

The cover letter should be concise, highlight relevant skills, and express genuine interest. Do not include placeholder brackets. Output only valid JSON.
"""

    if settings.use_local_llm:
        # Use Ollama
        try:
            response = requests.post(
                f"{settings.local_llm_url}/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False, "format": "json"},
                timeout=60
            )
            response.raise_for_status()
            result = response.json()["response"]
            data = json.loads(result)
        except Exception as e:
            # Fallback to mock response if LLM fails
            return mock_cover_letter(job_description)
    else:
        client = OpenAI(api_key=settings.openai_api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(completion.choices[0].message.content)

    return CoverLetterResponse(**data)

def mock_cover_letter(job_description: str) -> CoverLetterResponse:
    """Fallback mock generator when LLM is unavailable."""
    return CoverLetterResponse(
        cover_letter="Dear Hiring Manager,\n\nI am writing to express my strong interest in the position. My background aligns well with the requirements, and I'm excited about the opportunity to contribute to your team.\n\nSincerely,\n[Your Name]",
        explanation="Your resume demonstrates relevant skills and experience that match key aspects of the job description.",
        suggestions=["Tailor your resume to highlight specific achievements mentioned in the job description.", "Consider adding metrics to demonstrate impact."]
    )