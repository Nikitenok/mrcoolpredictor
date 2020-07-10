from django.db import models


class Task(models.Model):
    title = models.CharField('Name', max_length=50)
    task = models.TextField('Description')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'


class Symbols(models.Model):
    id = models.IntegerField('Id', primary_key=True)
    sym = models.CharField('Symbol', max_length=15)

    def __str__(self):
        return self.sym


class DatePoints(models.Model):
    id = models.DateTimeField('Id', primary_key=True)
    close = models.FloatField('Close')
    sym = models.IntegerField('Symbol')

    def __str__(self):
        return self.sym