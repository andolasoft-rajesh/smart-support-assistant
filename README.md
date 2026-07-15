# smart-support-assistant

## Backend setup

The backend uses PostgreSQL with `pgvector`. You must start the database before running the FastAPI app.

### Run the database

From the repository root:

```powershell
docker-compose up -d
```

This starts PostgreSQL on `localhost:5432` with:
- database: `assistant`
- user: `postgres`
- password: `postgres`

### Create backend environment

Create a `backend/.env` file with:

```ini
DATABASE_URL=postgresql://postgres:ompriya1234@localhost:5432/assistant
GEMINI_API_KEY=your_api_key_here
```

### Start the backend

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

### Why this error occurred

Your crash is caused by the backend trying to open a PostgreSQL connection, but no server was accepting connections on `localhost:5432`.

If you see this again, verify that the database container is running and that port `5432` is available.
