FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Work from service directory so module "app" is importable
WORKDIR /workspace/main_directory/soap_server

# Install dependencies
COPY main_directory/soap_server/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy service code
COPY main_directory/soap_server /workspace/main_directory/soap_server

# Add entrypoint to seed DB before starting server
COPY main_directory/soap_server/entrypoint.sh /workspace/main_directory/soap_server/entrypoint.sh
RUN chmod +x /workspace/main_directory/soap_server/entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/workspace/main_directory/soap_server/entrypoint.sh"]
