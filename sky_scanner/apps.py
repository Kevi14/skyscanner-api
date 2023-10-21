from django.apps import AppConfig

class SkyScannerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sky_scanner'

    def ready(self):
        import sky_scanner.signals
