<div align="center">

# 🤖 AutoApply AI — Intelligent Job Application System

[![CI](https://github.com/Nersisiian/Autoapply-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Nersisiian/Autoapply-AI/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/Nersisiian/Autoapply-AI?style=social)](https://github.com/Nersisiian/Autoapply-AI)

**Stop filling out job applications manually.**  
Let AI find, match, and auto‑apply to jobs while you sleep — with personalized cover letters and a beautiful dashboard.

</div>

---

## 🔥 Why AutoApply AI?

Job hunting is broken:
- Hours wasted tailoring resumes
- Endless cover letter writing
- Repetitive form filling

**AutoApply AI changes everything:**
- **1‑command install** — docker-compose up
- **ML‑powered matching** — find jobs you're actually qualified for
- **AI cover letters** — GPT‑4 / Llama 3 writes personalized letters
- **🚀 Autopilot mode** — the bot works 24/7, applying to best‑fit jobs automatically

> *I woke up to 7 new applications the bot submitted for me. This is insane!* – Beta user

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Upload** | PDF/DOCX → parsed into skills, experience, embeddings |
| 🔍 **Job Aggregation** | Simulated feeds (extendable to Indeed, LinkedIn APIs) |
| 🎯 **ML Matching** | SentenceTransformers + cosine similarity → 0–100 fit score |
| ✍️ **AI Cover Letters** | GPT‑4 / Llama 3 generates tailored letters + improvement tips |
| 🤖 **Autopilot** | Set a threshold — the bot finds new jobs and auto‑applies |
| 📊 **Tracker** | View all applications, statuses, and notes |
| 🐳 **Docker Ready** | One command to start everything |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, SQLAlchemy, SQLite |
| ML/AI | SentenceTransformers, OpenAI / Ollama |
| Frontend | Streamlit |
| DevOps | Docker, docker-compose, GitHub Actions |

---

## 📦 Quick Start

### Prerequisites
- Docker & Docker Compose installed

  ash
git clone https://github.com/Nersisiian/Autoapply-AI.git
cd Autoapply-AI
cp .env.example .env
# (Optional) Add your OpenAI key to .env
docker-compose up --build
  

Open:
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

### 🧪 Using Local LLM (Ollama)
Uncomment the ollama service in docker-compose.yml and set USE_LOCAL_LLM=true in .env.

---

## 🖥️ Demo & Screenshots

| Upload Resume | Job Matches | Autopilot |
|---------------|-------------|-----------|
| ![upload](docs/upload.png) | ![matches](docs/matches.png) | ![autopilot](docs/autopilot.png) |

*(Place your actual screenshots in docs/ folder)*

---

## 🧠 How It Works (30 sec)

1. Upload resume → parsed & embedded.
2. Fetch jobs → each job embedded.
3. Cosine similarity ranks jobs by fit.
4. LLM generates cover letter for selected job.
5. Autopilot runs background scheduler, repeats steps 2‑4 automatically.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

**Ideas for contribution:**
- Add real job APIs (JSearch, SerpAPI)
- Integrate Playwright for real form submission
- Add more resume parsers (LinkedIn export)

---

## 📈 Roadmap

- [x] MVP with simulated jobs
- [x] Autopilot background scheduler
- [ ] Real job board integrations
- [ ] Browser automation (Playwright)
- [ ] Multi‑user support

See full roadmap in [ROADMAP.md](ROADMAP.md).

---

## 📄 License

MIT © [Nersisiian](https://github.com/Nersisiian)

---

<div align="center">
  ⭐ If you find this useful, please star the repo! ⭐
</div>
