FROM python:3.12-slim

# Without this, Python fully block-buffers stdout when it isn't a TTY
# (always true inside a container) — log lines (including the SDK's
# evidentrace stage logs) can sit unflushed instead of reaching
# `docker logs` as they're written.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app folder contents **directly into /app**
COPY app/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]