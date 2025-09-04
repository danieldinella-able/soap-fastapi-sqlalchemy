FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY services/rest_api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy app
COPY services/rest_api/rest_app /app/rest_app

EXPOSE 8000

CMD ["uvicorn", "rest_app.main:app", "--host", "0.0.0.0", "--port", "8000"]

