# TherapEase

TherapEase is a platform that helps in identifying location of special education facilities and services in the Philippines.

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

- **API**: The main API service handles the proxying of requests to the internal services like search. This also contains the data management and auth services. This developed using Django and Django Rest Framework.

- **UI**: The main UI service contains the map and search interfaces. This is being developed using VueJS and NuxtJS.

## Utils

The `utils` directory contains a variety of scripts that are used to work with the application. Please be advised that these scripts maybe outdated or some of them have deprecated functionality.

## Development

Development information can be found under the `docs` directory.

### Pre-commit
TherapEase requires to install the following:

- [pre-commit](https://pre-commit.com/)
- [ruff](https://docs.astral.sh/ruff/installation/)
- [black](https://github.com/psf/black)

Refer to the individual dependencies on how to install and set them up. These dependencies will validate the files at the commit stage `git commit -m`.

### Running Tests

- API: `python manage.py test`

### TODO
- Setup a testing framework for the frontend.
