# Mini Project Management System

Full-stack mini project management system built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, and a Next.js frontend.

## Architecture

### Backend

The backend follows a layered architecture inside [`backend/app`]:

- `routes`: HTTP endpoints/controllers
- `services`: business rules and transaction boundaries
- `repositories`: database access
- `models`: SQLAlchemy models
- `schemas`: Pydantic request and response models
- `core`: configuration, security, and exceptions
- `db`: engine, session, and base metadata
- `utils`: shared FastAPI dependencies

### Frontend

The frontend lives in [`frontend`] and uses the Next.js app router with:

- JWT stored in `localStorage`
- Axios instance with auth header injection
- Login page
- Project list page
- Task list with filtering and pagination
- Create task modal

## Features

- JWT auth with register and login
- Password hashing with bcrypt via Passlib
- Role-aware access controls
- Project CRUD
- Task create, update, list with filtering and pagination
- Alembic migration for initial schema
- Docker setup for database, backend, and frontend
- FastAPI Swagger docs at `/docs`
- Basic pytest coverage for security helpers and task filter schema
- Postman collection in [`postman_collection.json`](/F:/MINI%20PROJECT/postman_collection.json)

## API Summary

### Auth

- `POST /auth/register`
- `POST /auth/login`

### Users

- `POST /users` admin only
- `GET /users` authenticated users

### Projects

- `POST /projects` admin only
- `GET /projects` authenticated users
- `PUT /projects/{id}` admin only
- `DELETE /projects/{id}` admin only

### Tasks

- `POST /tasks`
- `PUT /tasks/{id}`
- `GET /tasks`

Task filtering and pagination examples:

- `/tasks?status=todo`
- `/tasks?project_id=1`
- `/tasks?assigned_to=2`
- `/tasks?page=1&limit=10`

## Setup

### Option 1: Docker

1. Copy [`.env.example`](/F:/MINI%20PROJECT/.env.example) to `.env`.
2. From the project root, run `docker compose up --build`.
3. Open:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - Swagger docs: `http://localhost:8000/docs`

### Option 2: Local development

#### Backend

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Configure a PostgreSQL database and set env vars in `.env`.
4. Run migrations:

```bash
cd backend
alembic upgrade head
```

5. Start the backend:

```bash
cd backend
uvicorn app.main:app --reload
```

#### Frontend

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start the frontend:

```bash
cd frontend
npm run dev
```

## Environment Variables

Example values are in [`.env.example`](/F:/MINI%20PROJECT/.env.example):

- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `NEXT_PUBLIC_API_URL`

## Testing

Run backend tests with:

```bash
cd backend
pytest
```

## Notes

- The app expects PostgreSQL in normal operation; tests are lightweight unit tests and do not require the database.
- The first account created via `POST /auth/register` becomes an admin so a fresh setup can bootstrap itself. Later registrations default to developer.
