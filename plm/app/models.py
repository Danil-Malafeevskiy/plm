from django.contrib.gis.db import models
from django.contrib.auth.models import Group, AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class Type(models.Model):
    name = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=100, default="")
    headers = ArrayField(models.JSONField())
    properties = ArrayField(models.CharField(max_length=100), blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    image = models.BinaryField(blank=True, default="".encode('utf-8'))

class Feature(models.Model):
    name = models.ForeignKey(Type, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=100, blank=True, default="Feature")
    properties = models.JSONField()
    geometry = models.GeometryField()
    image = models.BinaryField(blank=True, default="".encode('utf-8'))

class User(AbstractUser):
    image = models.BinaryField(blank=True, default="".encode('utf-8'))

class VersionControl(models.Model):
    user = models.TextField(default="admin")
    date_update = models.DateTimeField(default=timezone.now)
    version = models.JSONField(blank=True, null=True)
    new_version = models.JSONField(blank=True, null=True)
    dataset = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    comment = models.CharField(max_length=100, default="", blank=True)
    flag = models.BooleanField(default=False)

class Ruls(models.Model):
    type_1 = models.ForeignKey(Type, on_delete=models.CASCADE)
    type_2 = models.ForeignKey(Type, on_delete=models.CASCADE)