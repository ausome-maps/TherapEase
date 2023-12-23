# Architecture Notes

The general architecture will consist of an API and client services. The following are the general features of the TherapEase platform.

- Geospatial lookup from DB that will require the following parameters bounding box - upper left and lower right in decimal degrees and/or the name of the facility.
- Ingestion layer that pulls new nodes or updates from OSM data.
- Publishing layer that pushes new nodes or updates to OSM.
- Authentication and authorization layer
- Login mechanism
- Entity/facility information management
- Payment and scheduling system
- Map dashboard which allows for filtering and viewing of facility/entity information
- Geocoding service/api

I will be using the following tool https://www.drawio.com/ to create the architecture and other diagrams.

The initial diagram is located here: https://drive.google.com/file/d/10JHxEi-_yzdSq5LcPkDmZmh81TTSzLHW/view?usp=drive_link

Initial Architecture:
![TherapEaseDiagrams-Architecture](https://github.com/ausome-maps/TherapEase/assets/6139863/63722273-23c0-48d7-9050-a364eaa7506d)
