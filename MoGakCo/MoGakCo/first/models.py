from django.db import models

# Create your models here.


class Time(models.Model):
    next_time = models.DateTimeField()


class Ranking(models.Model):
    user_ip = models.CharField(max_length=100, default='0.0.0.0')
    user_name = models.CharField(max_length=100)
    time = models.DateTimeField()

    class Meta:
        ordering = ['time']
