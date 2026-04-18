# Contributing to AutoApply AI

Thanks for your interest in contributing!

## How to contribute

1. Fork the repo.
2. Create a feature branch (git checkout -b feature/amazing-feature).
3. Commit your changes (git commit -m 'Add amazing feature').
4. Push to the branch (git push origin feature/amazing-feature).
5. Open a Pull Request.

## Development setup

  ash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz

# Frontend
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
  

## Code style
- Follow PEP 8 for Python.
- Use type hints where possible.

## Reporting bugs
Open an issue with steps to reproduce and environment details.

Thank you!
