# TherapEase

TherapEase is a platform that helps in identifying location of special education facilities and services in the Philippines.

## General Execution

The entire platform can be run using `Docker` using `docker compose`. Refer to the `docker-compose.yml` for the extensive list of services.

### Requirements

- Docker
- docker compose

## Services

- **Gateway**: The gateway service handles the proxying of requests to the internal services like geocoding and search.

- **Geocoding**: The main geocoding service handles the translation of place names into actual latitude and longitude coordinates. This is powered by `Nominatim`.
