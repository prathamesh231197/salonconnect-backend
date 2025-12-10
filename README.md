# SalonConnect - Backend (FastAPI)

This repository contains the backend API for **SalonConnect** — a booking/marketplace app connecting local barbers/salons with customers.

## What is included in this commit

- FastAPI backend with JWT authentication (register/login)
- SQLAlchemy models for `User`, `Salon`, `Service`
- Endpoints:
  - `POST /api/auth/register`
  - `POST /api/auth/login`
  - `GET /api/health`
  - `GET /api/users/me` (protected)
  - `POST /api/salons` (protected - creates salon and nested services)
  - `GET /api/salons`
  - `GET /api/salons/{id}`
- Docker + docker-compose for local dev with PostgreSQL
- Example PowerShell snippets for testing endpoints (Windows)

## Quick start (Docker)

1. Build & run:

```bash
docker compose up --build


##How to test

##Register
Invoke-WebRequest -Uri "http://localhost:8000/api/auth/register" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"email":"alice@example.com","password":"password123","name":"Alice"}'


##get current user
$token = "<paste token>"
Invoke-WebRequest -Uri "http://localhost:8000/api/users/me" -Method GET -Headers @{ "Authorization" = "Bearer $token" } -UseBasicParsing



##Project layout
backend/
├─ app/
│  ├─ main.py
│  ├─ api/
│  │  └─ v1/
│  ├─ core/
│  ├─ crud/
│  ├─ db/
│  └─ schemas.py
├─ Dockerfile
├─ docker-compose.yml
└─ requirements.txt
```

---

### `docs/PROJECT_DOCS.md` (developer doc / changelog)

Create a `docs` folder and inside it `PROJECT_DOCS.md`:

```markdown
# Project Documentation — SalonConnect Backend

## Overview

This document captures design decisions, features implemented in this commit, and next steps.

### Implemented features (commit up to this point)

- Authentication: JWT-based login and register
- User model with role support
- Salon and Service models with CRUD (create + list + get)
- Password hashing using Passlib (pbkdf2_sha256)
- Docker + PostgreSQL dev environment
- Basic error-handling and validations

### API Endpoints (summary)

- `GET /api/health` — health check
- `POST /api/auth/register` — create user, returns JWT
- `POST /api/auth/login` — login, returns JWT
- `GET /api/users/me` — current user (requires Bearer token)
- `POST /api/salons` — create a salon (requires Bearer token)
- `GET /api/salons` — list salons
- `GET /api/salons/{id}` — get salon details

### Data model notes

- Users: id, email, hashed_password, name, phone, role, created_at
- Salons: owner_id -> users.id, business details, lat/lng, phone
- Services: salon_id -> salons.id, name, duration, price

### How to run locally

(see README.md)

### Known limitations / TODO

- No Alembic migration support (using `create_all` currently)
- No email verification
- No RBAC enforcement beyond token presence (we will later restrict some endpoints to `role == "barber"`)
- No file/image uploads yet
- No tests

### Next development priorities

1. Implement booking/slot management (core app feature)
2. Add Alembic and migrations
3. Add tests (pytest)
4. Add role-based access control & owner verification
5. Build Flutter client and connect to endpoints
6. Add CI pipeline (lint, tests, build docker)

## Contacts / repo

- Developer: (your name)
- Repo: (link to repository once pushed)
```
