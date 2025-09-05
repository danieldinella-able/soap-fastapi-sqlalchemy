FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Keep repository root on PYTHONPATH so imports like
# "main_directory.rest_api.rest_app.*" resolve correctly
ENV PYTHONPATH=/workspace
WORKDIR /workspace

# Install dependencies
COPY main_directory/rest_api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project code (what the app imports)
COPY app /workspace/app
COPY main_directory /workspace/main_directory

EXPOSE 8000

CMD ["uvicorn", "main_directory.rest_api.rest_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
