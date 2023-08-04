# TherapEase

TherapEase is a platform that helps in identifying location of special education facilities and services in the Philippines.

## General Execution

The entire platform can be run using `Docker` using `docker compose`. Refer to the `docker-compose.yml` for the extensive list of services.

1. Run docker compose up

   ```bash
   docker compose up
   ```

2. The API service can be accessed through a browser with the following URL http://localhost:9001. _You may refer to http://localhost:9001/docs for the list of available APIs._

3. The UI or client service can be accessed through a browser with the following URL http://localhost:9002.

### Requirements

- [Docker](https://docs.docker.com/desktop/wsl/)
- [docker compose](https://docs.docker.com/compose/install/)

## Services

- **API**: The main API service handles the proxying of requests to the internal services like geocoding and search.

- **Geocoding**: The main geocoding service handles the translation of place names into actual latitude and longitude coordinates. This is powered by `Nominatim`. Can be accessed by `http://localhost:9001/geocode?q=<placename>`

- **Search**: The search service handles the indexing of the facilities information.

## Development

Development information can be found under the `docs` directory.

## Utils

The `utils` directory contains a variety of scripts that are used to work with the application.
