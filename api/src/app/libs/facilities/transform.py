from typing import Dict


def transform_es_result_to_geojson(es_queries: Dict[str, dict]) -> Dict[str, dict]:
    """
    Transforms an ElasticSearch result into a GeoJSON object.

    Args:
        es_queries (dict): A dictionary containing the ElasticSearch query results.

    Returns:
        dict: A GeoJSON object representing the transformed result.
    """

    geojson: Dict[str, any] = {
        "type": "FeatureCollection",
        "name": "Ausome Maps - Therapy Centers",
        "features": [],
        "total": {"value": 0, "relation": "eq"},
    }
    try:
        geojson["total"] = es_queries["hits"]["total"]
        # Add features to geojson.
        for es_query in es_queries["hits"]["hits"]:
            data = es_query["_source"].copy()
            data["id"] = es_query["_id"]
            geojson["features"].append(data)
    except:
        pass
    return geojson
