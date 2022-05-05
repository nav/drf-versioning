from django.apps import AppConfig
from api import versions
from catalogue import transformations


class CatalogueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalogue"

    def ready(self):
        versions.v1.register_transformation(transformations.RenameProductSKUToName)
        versions.v2.register_transformation(transformations.RenameProductNameToTitle)
