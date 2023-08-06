# coding: utf-8

from django.core.management.base import BaseCommand

from django_beatle.conf import settings
from django_beatle.models import Task


class Command(BaseCommand):
    help = 'Sync beatle tasks from config to database'

    def handle(self, *args, **options):
        conf_tasks = settings.get_configuration().get('TASKS', [])
        db_tasks = dict(Task.objects.values_list('path', 'frequency'))

        for path, frequency in conf_tasks.items():
            if path not in db_tasks:
                task = Task(path=path, frequency=frequency)
                task.save()
