from django.apps import AppConfig
from django.db.utils import ProgrammingError

from .conf import settings


class BeatleConfig(AppConfig):
    name = 'django_beatle'
    verbose_name = 'Django Beatle'

    def ready(self):
        try:
            from .models import Task

            conf_tasks = settings.get_configuration().get('TASKS', [])
            db_tasks = dict(Task.objects.values_list('path', 'frequency'))

            for path, frequency in conf_tasks.items():
                if path not in db_tasks:
                    task = Task(path=path, frequency=frequency)
                    task.save()

        # no initial migration yet
        except ProgrammingError:
            pass

