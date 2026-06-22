FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --gid 10001 appgroup && \
    useradd --uid 10001 --gid appgroup --shell /bin/bash --create-home appuser

COPY pyproject.toml ./
COPY src/ ./src/

RUN pip install --no-cache-dir -e .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "falcon_grounds.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
