# documents.py

from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from django.forms.models import model_to_dict
from .models import Facilities


@registry.register_document
class FacilitiesDocument(Document):
    geometry = fields.ObjectField()
    properties = fields.ObjectField()

    class Index:
        # Name of the Opensearch index
        name = "facilities"
        # See Opensearch Indices API reference for available settings
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Facilities  # The model associated with this Document

        # The fields of the model you want to be indexed in Opensearch
        fields = [
            "id",
        ]
        ordering = ["properties.osm_id"]
        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000

    def prepare_geometry(self, instance):
        return instance.geometry

    def prepare_properties(self, instance):
        return model_to_dict(instance.properties)
