# AGENTS.md — TherapEase

## Project Overview

TherapEase is a full-stack web app for locating special education facilities and services in the Philippines. It is a **monorepo** with a Django REST backend (`api/`) and a Nuxt 4 SPA frontend (`client/`), orchestrated via Docker Compose.

## Architecture

```
Browser ──> Traefik (reverse proxy) ──> Nuxt SPA (client/, port 9002)
                                    ──> Django REST API (api/, port 9001)
                                          ├── PostgreSQL 15 (db)
                                          ├── Redis 7 (cache/Celery broker)
                                          └── MinIO (S3-compatible storage)
```

- **Frontend**: Nuxt 4 (SSR off), Vue 3, TypeScript, Tailwind CSS v4, Flowbite v4, Leaflet maps
- **Backend**: Django 5.2 LTS, DRF, Djoser, simplejwt, celery, django-opensearch-dsl
- **Infra**: Docker Compose (dev), Ansible + Traefik (prod), GitHub Actions CI

## Directory Layout

```
api/                        Django backend
  apps/core/facilities/     Facility model, views, search, permissions
  apps/core/users/          User/Profile/Organization models, auth, JWT
  django_app/               Settings, URL conf, celery, WSGI/ASGI
client/                     Nuxt frontend
  assets/css/               Tailwind entry point
  components/Base/          AppHeader, AppFooter, AppDropdown, etc.
  components/Details/       Facility detail sub-components
  components/Search/        Search results listing components
  composables/useAuth.ts    Auth composable (login, register, JWT, profile)
  layouts/default.vue       Default layout wrapper
  middleware/auth.global.ts  Global auth route guard
  pages/                    Page components (index, search, details, login, etc.)
docs/                       Architecture, auth, data model, search, UI docs
infrastructure/             Ansible playbooks + Traefik configs
utils/                      Python data-loading scripts
```

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 22+ (for local frontend dev outside Docker)
- Python 3.12 (for local backend dev outside Docker)

### Quick Start
```bash
# Copy env file and fill in values
cp .env.sample .env

# Start all services
docker compose up
```

Exposed ports:
- Frontend: http://localhost:9002
- API: http://localhost:9001
- Swagger docs: http://localhost:9001/docs/
- MinIO console: http://localhost:9003

### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```
Runs on each commit: Black (Python formatting), Ruff (lint + format), check-yaml, trailing-whitespace.

## Common Commands

### Backend (run from `api/`)

| Command | Description |
|---|---|
| `python manage.py runserver 0.0.0.0:8000` | Dev server |
| `python manage.py test` | Run all tests |
| `python manage.py test apps.core.facilities.tests` | Run specific test module |
| `python manage.py makemigrations` | Create new migrations |
| `python manage.py migrate` | Apply migrations |
| `python manage.py shell` | Django shell |

### Frontend (run from `client/`)

| Command | Description |
|---|---|
| `npm run dev` | Nuxt dev server |
| `npm run build` | Production build → `.output/` |
| `npm run generate` | Static site generation |
| `npm run preview` | Preview production build |

## Testing

### Backend Tests
Tests use Django's `TestCase` and DRF's `APITestCase`. Test files:
- `api/apps/core/users/tests.py` — User auth, profile CRUD, organization permissions, JWT
- `api/apps/core/facilities/tests.py` — Facility CRUD and search

```bash
cd api && python manage.py test
```

### Frontend Tests
No frontend testing framework is configured yet (noted as TODO in README).

### CI
GitHub Actions run backend tests with PostgreSQL + Redis service containers on push/PR to `main`. Frontend CI only builds the Docker image.

## Key Patterns & Conventions

### Backend (Django)

- **Settings**: `api/django_app/settings.py` — all config via `os.environ.get()`.
- **Auth**: JWT via `djangorestframework-simplejwt`; user management via `djoser`; social login (Google/Facebook) via `python-social-auth`.
- **Permissions**: Each app has a `permissions.py` with custom DRF permission classes.
- **Signals**: `signals.py` in each app handles auto-creation (e.g., Profile on User create, Facilities on FacilityProperties create).
- **Background tasks**: Celery with Redis broker. Worker schedule defined in `api/django_app/celery.py`.
- **Logging**: JSON-formatted logs via `django_app/log_formatter.py`.
- **API tracking**: `drf-api-tracking` middleware logs all API requests.
- **Search**: Full-text search via `django-opensearch-dsl`; endpoint at `POST /facilities/search`.
- **Superuser auto-create**: `entrypoint.sh` creates `admin@sample.com / adminpassword012` if it doesn't exist.
- **Migrations**: Always run `makemigrations` after model changes and commit the migration files.

### Frontend (Nuxt/Vue)

- **SSR is OFF** (`ssr: false` in `nuxt.config.ts`). This is a client-side SPA.
- **Auth**: JWT tokens stored in localStorage, managed by `client/composables/useAuth.ts`. Tokens auto-refreshed. Protected routes guarded by `middleware/auth.global.ts`.
- **State**: No Vuex/Pinia — auth state is a simple reactive composable.
- **API calls**: Uses `$fetch` (Nuxt's built-in HTTP client). API base URL configured via `runtimeConfig.public.API_BASE_URL`.
- **Styling**: Tailwind CSS v4 (`@import "tailwindcss"` in `assets/css/input.css`). Flowbite v4 components. Custom Lato font.
- **Components follow Vue 3 Composition API** with `<script setup lang="ts">`.
- **Pages are file-based** routed via Nuxt's `pages/` directory.
- **Deprecated code**: `deprecated/AppFilter.vue` — do not modify, use `components/Search/AppFilter.vue` instead.

### Infrastructure

- **Environment variables** managed via `.env` file (gitignored). Template at `.env.sample`.
- **Docker Compose** defines 5 services: `frontend`, `api`, `db` (Postgres 15), `cache` (Redis 7), `storage` (MinIO).
- **Traefik** handles routing in both dev (`infrastructure/traefik/traefik.dev.toml`) and prod.
- **Ansible** playbooks in `infrastructure/ansible/playbooks/` for production deployment.

## API Overview

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/facilities/` | GET/POST | Auth (CRUD) | List/create facilities |
| `/api/facilities/{id}/` | GET/PUT/DELETE | Auth | Facility detail |
| `/api/facilities/search` | POST | Public | Full-text search with filters |
| `/api/profile/` | GET/PATCH | Auth | User profile |
| `/api/organization/` | GET/POST | Auth | Organizations |
| `/api/auth/jwt/create/` | POST | Public | Get JWT tokens |
| `/api/auth/jwt/refresh/` | POST | Public | Refresh JWT access token |
| `/api/auth/users/` | POST | Public | Register user |
| `/api/auth/users/activation/` | POST | Public | Activate user account |
| `/api/social/{google,facebook}/` | POST | Public | Social login |

## Important Notes

- The `api/apps/custom/` and `api/apps/plugins/` directories are placeholders for future apps.
- Backups directory (`api/backups/`) is gitignored except for `.gitkeep`.
- The `api/app.log` and `api/requests.log` files are gitignored but may exist locally.
- When adding new Django models, create the app under `api/apps/core/` or `api/apps/custom/` as appropriate.
- The data model for facilities is detailed in `docs/data_model.md` — consult it before modifying facility schemas.
- `social-core` and `social-auth-app-django` are used for social auth but not listed in `requirements.txt` directly (installed as dependencies).
- This project has **no linter or typecheck script** for the frontend — TypeScript checking happens via `nuxt dev` / `nuxt build` automatically.
