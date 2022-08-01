from django.contrib.gis.db import models
from django.contrib.auth.models import Group

class Feature(models.Model):
    name = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True, default="Feature")
    properties = models.JSONField()
    geometry = models.GeometryField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=2)
