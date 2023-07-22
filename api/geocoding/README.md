# Geocoding Service
The geocoding service of TherapEase uses `Nominatim` as the foundation service.

## Requirements
- Docker

## How to Run

```bash
docker run -it \
  -e PBF_URL=https://download.geofabrik.de/asia/philippines-latest.osm.pbf \
  -e REPLICATION_URL=https://download.geofabrik.de/asia/philippines-updates/ \
  -p 8080:8080 \
  --name therapease_nominatim \
  mediagis/nominatim:4.2

```