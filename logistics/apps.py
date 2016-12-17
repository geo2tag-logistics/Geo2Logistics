from django.apps import AppConfig

from logistics.Geo2TagService import clearAllFleets


class LogisticsServiceConfig(AppConfig):
    name = 'logistics'
    verbose_name = "Logistics Service"

    def ready(self):
        print("Application startup execution")
        clearAllFleets()
