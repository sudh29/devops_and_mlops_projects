# Production Dockerfile for FastAPI MLOps Model Serving
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

# Create unprivileged service user and install curl for healthcheck
RUN useradd -m -u 1000 mluser && \
    apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /root/.local /home/mluser/.local
COPY . /app

ENV PATH=/home/mluser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

RUN chown -R mluser:mluser /app
USER mluser

EXPOSE 8000

HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "serving.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
