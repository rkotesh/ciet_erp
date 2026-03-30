from django.apps import AppConfig


class ParentsConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'apps.parents'
