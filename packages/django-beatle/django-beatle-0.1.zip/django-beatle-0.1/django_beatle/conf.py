# coding: utf-8

import importlib
import os

from django.conf import settings as django_settings


django_settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")
DEFAULT_CONFIG_MODULE = '.'.join([django_settings_module.rsplit('.', 1)[0], 'beatleconf'])


DEFAULT_SETTINGS = {
    'SECRET_KEY': None,
    'TIME_ZONE': 'Europe/Moscow'
}


class ImproperlyConfigured(Exception):
    pass


class Settings:
    def __init__(self):
        self.load()

    def load_defaults(self):
        for setting, value in DEFAULT_SETTINGS.items():
            setattr(self, setting, value)

    def load(self):
        self.load_defaults()

        module_name = getattr(django_settings, 'BEATLE_CONFIG_MODULE', DEFAULT_CONFIG_MODULE)
        module = importlib.import_module(module_name)
        for setting in dir(module):
            if setting.isupper():
                value = getattr(module, setting)
                setattr(self, setting, value)

        if not self.SECRET_KEY:
            raise ImproperlyConfigured('SECRET_KEY is required')

    def get_configuration(self):
        return {
            setting: getattr(self, setting) for setting in dir(self)
            if setting.isupper() and setting != 'SECRET_KEY'
        }


settings = Settings()
