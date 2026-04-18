# 🤖 AutoApply AI — Intelligent Job Application System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Stop filling out job applications manually.**  
Upload your resume once, and let AI find, match, and apply to jobs for you — with personalized cover letters and a beautiful dashboard.

<p align="center">
  <img src="https://via.placeholder.com/800x400?text=AutoApply+AI+Dashboard" alt="Dashboard Screenshot" />
</p>

## 🔥 Why This Matters

Job hunting is broken. You spend hours tailoring resumes, writing cover letters, and filling repetitive forms. AutoApply AI automates the grunt work while keeping you in control. It's not spam — it's a smart assistant that helps you apply to jobs you're actually qualified for.

## ✨ Features

- **Resume Upload & Parsing**: Drag & drop PDF/DOCX → parsed into structured data and embeddings.
- **Job Aggregation**: Simulated feeds (or connect to real APIs like JSearch, SerpAPI).
- **ML-Powered Matching**: SentenceTransformers + cosine similarity → ranked jobs 0–100 fit score.
- **AI Cover Letters**: GPT-4 / Llama 3 generates personalized letters with "why you're a match".
- **🚀 Autopilot Mode**: Set a fit threshold, and the system will **automatically** find new jobs, generate cover letters, and record applications in the background.
- **Safe Auto-Apply**: Simulates form submission; you review before any real action.
- **Application Tracker**: See all applied jobs, status, and notes.

## 🛠️ Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Backend     | FastAPI, SQLAlchemy, SQLite         |
| ML / AI     | SentenceTransformers, OpenAI / Ollama |
| Frontend    | Streamlit                           |
| DevOps      | Docker, docker-compose              |

## 📦 Quick Start

### Prerequisites
- Docker and Docker Compose installed.

### Run with Docker (recommended)
```bash
git clone https://github.com/yourusername/autoapply-ai.git
cd autoapply-ai
cp .env.example .env
# Edit .env to add your OpenAI key (or keep local LLM)
docker-compose up --build