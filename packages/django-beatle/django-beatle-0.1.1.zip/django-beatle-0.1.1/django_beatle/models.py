# coding: utf-8

from django.db import models


class Task(models.Model):
    path = models.CharField(max_length=255, unique=True, verbose_name='function path')
    frequency = models.CharField(max_length=255, verbose_name='cron config')
    is_enabled = models.BooleanField(default=True, verbose_name='is enabled')

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __unicode__(self):
        return self.path
