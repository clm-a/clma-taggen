FROM python:3.11.10 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m venv .venv
COPY ./requirements.txt ./
RUN .venv/bin/pip install -r requirements/w2v_api_serving.txt

FROM python:3.11.4-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
CMD ["/app/.venv/bin/gunicorn", "-w", "4", "tags_generator.server:app", "-b", "0.0.0.0:8080"]
