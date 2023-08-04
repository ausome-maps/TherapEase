def transform_es_result_to_geojson(es_queries):
    """
    Transforms ES results into GeoJSON. This is a helper function to be used by the geospatial_search module.

    @param es_queries - List of ES queries returned by ElasticSearch

    @return GeoJSON representation of the ES queries
    """
    geojson = {
        "type": "FeatureCollection",
        "name": "Ausome Maps - Therapy Centers",
        "features": [],
        "total": {"value": 0, "relation": "eq"},
    }
    try:
        # Add features to geojson.
        for es_query in es_queries["hits"]["hits"]:
            data = es_query["_source"].copy()
            data["id"] = es_query["_id"]
            geojson["features"].append(data)
        geojson["total"] = es_queries["hits"]["total"]
    except:
        pass
    return geojson
