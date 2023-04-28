from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StarWarsConfig(AppConfig):
    name = "superdevs.starwars"
    verbose_name = _("StarWars")

    def ready(self):
        try:
            import superdevs.starwars.signals  # noqa: F401
        except ImportError:
            pass
