"""
App configuration model
"""
from django.apps import AppConfig


class TahoeSitesConfig(AppConfig):
    """
    Configuration model
    """
    name = 'tahoe_sites'

    def ready(self):
        """
        Import signals when the app is ready
        """
        from tahoe_sites import signals  # pylint: disable=import-outside-toplevel,unused-import
