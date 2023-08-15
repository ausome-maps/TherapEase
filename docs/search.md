# Search

The following are the examples on how query the Therapease Search Module.

There are 2 ways in implementing a query:

- GET using the query params through the variable `q` by using the full text query.
- POST using the data params by using the Opensearch filter [guidelines](https://opensearch.org/docs/1.2/opensearch/query-dsl/bool/)

1. Search using the Full Text capabilities
   ```
   curl -X GET http://localhost:9001/facilities?q=Manila
   ```
2. Search using the filters
   ```
   curl -X POST http://localhost:9001/facilities -d '{"query": {"bool": {"filter": { "match":  { "properties.city": "Manila" }}}}}'
   ```
   Since the metadata is stored under `properties` you will need to do the filter `properties.<filterName>`
