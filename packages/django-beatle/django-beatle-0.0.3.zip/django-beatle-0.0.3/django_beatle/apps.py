from django.apps import AppConfig, apps

from .conf import settings


class BeatleConfig(AppConfig):
    name = 'django_beatle'
    verbose_name = 'Django Beatle'

    def ready(self):
        try:
            Task = apps.get_model(app_label='django_beatle', model_name='Task')
            conf_tasks = settings.get_configuration().get('TASKS', [])
            db_tasks = dict(Task.objects.values_list('path', 'frequency'))

            for path, frequency in conf_tasks.items():
                if path not in db_tasks:
                    task = Task(path=path, frequency=frequency)
                    task.save()
        except Exception:
            pass
