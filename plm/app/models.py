from django.contrib.gis.db import models
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import ArrayField

class Dataset(models.Model):
    name = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=100, default="")
    headers = ArrayField(models.JSONField())
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)

class Feature(models.Model):
    name = models.ForeignKey(Dataset, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=100, blank=True, default="Feature")
    properties = models.JSONField()
    geometry = models.GeometryField()