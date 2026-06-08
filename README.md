
# Project Management System

## Architecture

Frontend: Next.js
Backend: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy
Migrations: Alembic

Flow:
Client (Next.js) -> FastAPI API -> SQLAlchemy -> PostgreSQL

Authentication uses JWT Access Token and Refresh Token stored in HTTP-only cookies.

## ER Diagram

Users
- id (PK)
- name
- email
- password
- role

Projects
- id (PK)
- name
- description
- created_by (FK -> users.id)

Tasks
- id (PK)
- title
- description
- status
- project_id (FK -> projects.id)
- assigned_to (FK -> users.id)
- due_date

Relationships:
- One User creates many Projects
- One Project contains many Tasks
- One User can be assigned many Tasks

## Setup Steps

### Backend

1. Create virtual environment
   python -m venv venv

2. Activate environment

3. Install dependencies
   pip install -r requirements.txt

4. Configure .env

5. Run migrations
   alembic upgrade head

6. Start server
   uvicorn main:app --reload

### Frontend

1. Install packages
   npm install

2. Run frontend
   npm run dev

## API Documentation

### Auth
POST /auth/login
GET /auth/me
POST /auth/refresh
POST /auth/logout

### Users
POST /users/
GET /users/
GET /users/{id}
PATCH /users/{id}
DELETE /users/{id}

### Projects
POST /projects/
GET /projects
GET /projects/{id}
PUT /projects/{id}
DELETE /projects/{id}

### Tasks
POST /tasks/
GET /tasks
GET /tasks/{id}
GET /tasks/project/{project_id}
PUT /tasks/{id}
DELETE /tasks/{id}


