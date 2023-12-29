# Search

The following are the examples on how query the Therapease Search Module.

1. General Search
   ```
   curl -X POST http://localhost:9001/facilities/search -d '{"q": "Manila"}'
   ```
   The query above will look the information into the following fields:
      - osm_id
      - placename
      - address
      - region
      - city
2. Search with Additional Filters
   ```
   curl -X POST http://localhost:9001/facilities/search -d '{"q": "Manila", "filters": {"services_offered": [{"orthoses": {"mode": {"onsite": 0, "teletherapy": 0, "home_service": 0}}}]}}'
   ```
   The additional `filters` query currently only supports the `services_offered` field.

