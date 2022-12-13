from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Accounts'
    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        import Accounts.signals
        # Explicitly connect a signal handler.
       