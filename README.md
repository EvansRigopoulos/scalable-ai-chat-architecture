# 🤖 AI Chat App

A Dockerized AI Chat application built with:

- ⚡ FastAPI
- 🐘 PostgreSQL
- 🐳 Docker & Docker Compose
- 🧠 SQLAlchemy (Async)
- 🔁 Redis (optional for caching / sessions)

---

## 📦 Project Structure

- ├── app/
- ├── api/
  - └── routes.py
- ├── db/
  - └── database.py
- ├── models/
  - └── message.py
- ├── services/

  - └── chat_service.py
- └── main.py 
- ├── docker/
  - └── docker-compose.yml
  - └── Dockerfile
- ── requirements.txt
- ── .env
- ── .gitignore
- ── README.md


---

## 🧠 Prerequisites

Before running the project, ensure you have:

✔ Docker and Docker Desktop installed and running  
✔ A Redis Cloud database (optional — for memory/RAG)  
✔ PostgreSQL connections configured via Docker  

---

## ✅ Environment File

Create a `.env` file at the project root with:

```env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=chatdb
DATABASE_URL={URL}

# Redis Cloud (optional)
REDIS_URL=redis:{URL}

🐳 Docker Compose

docker compose -f docker/docker-compose.yml up --build

a FastAPI app

a PostgreSQL database

pgAdmin for DB management

docker compose -f docker/docker-compose.yml up --build

After this runs, you should see:

FastAPI: http://localhost:8000

Swagger docs: http://localhost:8000/docs

pgAdmin: http://localhost:8080


Login to pgAdmin with:

Username: admin@admin.com
Password: admin


Connect to the database with:

Host: db
Port: 5432
User: postgres
Password: postgres
Database: chatdb

🔌 API Endpoints
🆗 Health
GET /health

Returns:

{"status": "ok"}

💬 Chat
POST /chat

Body:

{
  "user_id": "123",
  "message": "Hello!"
}

🧠 Optional Redis Memory (RAG)

If you set REDIS_URL in .env, your app will:

store recent user + assistant messages

build a short context for RAG-style responses

This is optional but recommended for “context aware” chat.


📐 Design Philosophy

This backend follows a scalable microservices-ready layout:

FastAPI for API layer

Async db + SQLAlchemy for persistence

Redis for cache/memory

Docker Compose for reproducible environments

🎯 Author

Evans Rigopoulos