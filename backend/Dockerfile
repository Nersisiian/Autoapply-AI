FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install en-core-web-sm==3.7.0
COPY . .
RUN mkdir -p /app/data/uploads
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
