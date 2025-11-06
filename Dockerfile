FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
ENV FLASK_APP=src/server/app.py PYTHONPATH=/app
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 8 --timeout 120 src.server.app:app

