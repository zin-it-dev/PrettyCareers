from django.apps import AppConfig


class ApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apis'
    verbose_name = 'PrettyTech 🎓'
    
    def ready(self):
        import apis.extensions, apis.signals