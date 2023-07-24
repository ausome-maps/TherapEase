# Geocoding Service

The geocoding service of TherapEase uses `Nominatim` as the foundation service.

## Requirements

- Docker
- Nominatim 4.2

## How to Run

This will run the `Nominatim` service using Docker. For a full list of parameters and other documentation refer to the following [link](https://github.com/mediagis/nominatim-docker/tree/master/4.2)

```bash
  docker run -it \
    -e PBF_URL=https://download.geofabrik.de/asia/philippines-latest.osm.pbf \
    -e REPLICATION_URL=https://download.geofabrik.de/asia/philippines-updates/ \
    -p 9000:8080 \
    --name therapease_nominatim \
    mediagis/nominatim:4.2

```

## Query Params

Example. `http://localhost:9080/?q=manila`

- q=<free-form query>
- amenity=<name and/or type of POI>
- street=<housenumber> <streetname>
- city=<city>
- county=<county>
- state=<state>
- country=<country>
- postalcode=<postalcode>
