# TherapEase

TherapEase is a platform that helps in identifying location of special education facilities and services in the Philippines.

## Features

- **Facility search** — Full-text search with filters (services, caters to, accreditation, delivery mode) on an interactive Leaflet map
- **Submit a facility** — Public multi-step wizard for submitting new facility data (basic info, contact, services, location picker with geocode search, image upload) — pending staff review
- **Admin submission dashboard** — Staff-only review pipeline: view, approve & merge, reject with notes, or delete submissions; filtered search with pagination
- **User accounts** — JWT-based authentication with registration, activation email, social login (Google/Facebook), profile management

## General Execution

The entire platform can be run using `Docker` using `docker compose`. Refer to the `docker-compose.yml` for the extensive list of services.

1. Make `entrypoints.sh` executable.

   ```bash
   chmod +x api/app/entrypoint.sh
   ```

2. Run docker compose up

   ```bash
   docker compose up
   ```

3. The API service can be accessed through a browser with the following URL http://localhost:9001. _You may refer to http://localhost:9001/docs/ for the list of available APIs._

4. The UI or client service can be accessed through a browser with the following URL http://localhost:9002.

### Requirements

- [Docker](https://docs.docker.com/desktop/wsl/)
- [docker compose](https://docs.docker.com/compose/install/)

## Services

- **API**: The main API service handles the proxying of requests to the internal services like search. This also contains the data management and auth services. Built with Python 3.12, Django 5.2 LTS, and Django Rest Framework.

- **UI**: The main UI service contains the map and search interfaces. Built with Node 22, Nuxt 4, Tailwind CSS v4, and Flowbite 4.

- **Database**: PostgreSQL 15.
- **Cache**: Redis 7.
- **Storage**: MinIO (official `minio/minio` image).

## Utils

The `utils` directory contains a variety of scripts that are used to work with the application. Please be advised that these scripts maybe outdated or some of them have deprecated functionality.

## Development

Development information can be found under the `docs` directory.

### Pre-commit
TherapEase uses the following pre-commit hooks (see `.pre-commit-config.yaml`):

- [pre-commit](https://pre-commit.com/)
- [ruff](https://docs.astral.sh/ruff/) v0.11
- [black](https://github.com/psf/black) 25.1

```bash
pip install pre-commit
pre-commit install
```

These will validate files automatically at the commit stage (`git commit`).

### Running Tests

- API: `python manage.py test`
- API (specific app): `python manage.py test apps.core.submissions.tests`
- Frontend: `cd client && npm run test` (Vitest — see `docs/TODO.md` #91)