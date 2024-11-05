from django.apps import AppConfig
from .signals import *


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        post_created()
        post_save()
