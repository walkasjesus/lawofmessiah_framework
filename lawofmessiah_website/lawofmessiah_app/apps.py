from django.apps import AppConfig

from lawofmessiah_app.translation import register_translations


class CommandmentsAppConfig(AppConfig):
    name = 'lawofmessiah_app'
    label = 'commandments_app'

    def ready(self):
        register_translations(self)
