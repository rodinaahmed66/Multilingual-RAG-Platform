# Multilingual RAG Platform

A high-performance **Retrieval-Augmented Generation (RAG)** system built with FastAPI. It demonstrates how to build an AI application that works with multiple database types (SQL and NoSQL) and multiple AI providers (OpenAI, Google, Cohere).

---

## Branch Overview

The project is organized into three branches, each representing a different stage of setup:

| Branch             | Database         | Setup Method                                       |
| :----------------- | :------------------- | :------------------------------------------------- |
| **`main`**         | **MongoDB** (NoSQL)  | **Hybrid:** Docker for DB + Manual Uvicorn for App |
| **`mini-rag`**     | **PostgreSQL** (SQL) | **Manual:** Requirements.txt + Local setup         |
| **`deployment-setup`** | **Full Stack**       | **Fully Automated:** One-click Docker Compose      |

---

## How to Run

### Branch 1 — `main` (MongoDB Version)

Use this for a NoSQL database setup.

1. Start the database container:
   ```bash
   docker-compose up -d mongodb
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```

---

### Branch 2 — `mini-rag` (PostgreSQL Version)

Use this for a traditional relational database setup.

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure PostgreSQL is installed on your machine.
3. Run database migrations:
   ```bash
   alembic upgrade head
   ```
4. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```

---

### Branch 3 — `deployment-setup` (Full Stack — Recommended)

The easiest way to run the project. Everything is automated.

1. Set up environment files:
   ```bash
   cd docker/env
   cp .env.example.app .env.app
   cp .env.example.postgres .env.postgres
   # Repeat for grafana and postgres-exporter
   ```
2. Launch all services at once:
   ```bash
   cd docker
   docker-compose up --build -d
   ```
   This starts the API, PostgreSQL, Qdrant (vector DB), Nginx, Prometheus, and Grafana — all together.

---

## Service URLs (deployment-setup branch)

| Service | URL |
| :--- | :--- |
| FastAPI App | http://localhost:8000 |
| Nginx (Production Entry) | http://localhost |
| Prometheus (Metrics) | http://localhost:9090 |
| Grafana (Dashboards) | http://localhost:3000 |
| Qdrant UI (Vector Storage) | http://localhost:6333/dashboard |

**Grafana Dashboards included:**
- FastAPI Observability
- Node Exporter (System)
- PostgreSQL Metrics

---

## Configuration

### Language

The system supports both **Arabic (`ar`)** and **English (`en`)**.

To change the default language, update your `.env` file:
```env
DEFAULT_LAN=ar   # or en
```

### AI Model (Generation Backend)

The project uses a **Factory Pattern** for LLMs — you can swap the AI model without changing any code. Update your `.env` file:

```env
GENERATION_BACKEND=OPENAI    # GPT-4 / GPT-3.5
GENERATION_BACKEND=GOOGLE    # Gemini Pro / Gemini Flash
GENERATION_BACKEND=COHERE    # Command-R models
```

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| Backend | FastAPI (Python) |
| Relational DB | PostgreSQL |
| NoSQL DB | MongoDB |
| Vector Storage | Qdrant, pgvector |
| AI Providers | OpenAI, Google Gemini, Cohere |
| Reverse Proxy | Nginx |
| Monitoring | Prometheus, Grafana |
| Containerization | Docker, Docker Compose |
| Dependency Management | uv |

---

## Docker Volume Management

Docker volumes keep your data safe even if containers are removed.

```bash
# List all volumes
docker volume ls

# Remove unused volumes
docker volume prune

# Back up a volume
docker run --rm -v <volume_name>:/volume -v $(pwd):/backup alpine tar cvf /backup/backup.tar /volume

# Full reset (removes all data)
docker compose down -v --remove-orphans
```

---

## Troubleshooting

### Connection Refused Error

If the FastAPI app shows `Connection refused`, it usually means the app started before the database was ready.

**Fix:** Restart only the app container:
```bash
docker compose restart fastapi
```

### Recommended Startup Order

For a more reliable start, bring up the databases first:
```bash
docker compose up -d pgvector qdrant
sleep 20
docker compose up -d
```

### Viewing Logs

```bash
docker compose logs -f fastapi
docker compose logs -f pgvector
```
