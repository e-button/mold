import django.utils.timezone as timezone

from django.db import models
from datetime import datetime
# Create your models here.

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Machine(models.Model):
    id = models.AutoField(primary_key=True)
    no = models.CharField(max_length=100)

class Process(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

class MoldData(models.Model):
    start_time = models.DateTimeField(default=datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    mod_no = models.CharField(max_length=100)