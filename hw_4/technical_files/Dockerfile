FROM python:3.9-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt из директории book_service
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# First copy the proto files
COPY /protos /app/protos/

# Create directory for generated protobuf files
RUN mkdir -p /app/posts_service/app/protos

# Generate proto files during build
# RUN python -m grpc_tools.protoc \
#     --proto_path=/app/protos \
#     --python_out=/app/posts_service/app/protos \
#     --grpc_python_out=/app/posts_service/app/protos \
#     /app/protos/*.proto

# Create __init__.py in the protos directory
RUN echo "# Generated protobuf modules" > /app/posts_service/app/protos/__init__.py

# Now copy the rest of the application
COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "posts_service.app.main"]

EXPOSE 50051 