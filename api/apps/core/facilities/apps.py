from django.apps import AppConfig


class FacilitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core.facilities"

    def ready(self):
        import apps.core.facilities.signals