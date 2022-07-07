from django.db import models
from django.contrib.postgres.fields import ArrayField

class Geometry(models.Model):
    type = models.CharField(max_length=100, blank=True, default="Point")
    coordinates = ArrayField(models.FloatField(), size=2)

class Tower(models.Model):
    name_tap = models.CharField(max_length=50, blank=True, default="-")
    number_support = models.IntegerField()
    VL = models.CharField(max_length=100, default="-")
    type_support = models.CharField(max_length=50)
    code_support = models.CharField(max_length=50, blank=True, default="Не определен")
    material = models.CharField(max_length=50)
    corner = models.FloatField()
    X = models.FloatField()
    Y = models.FloatField()
    Z = models.FloatField()
    shirota = models.FloatField()
    dolgota = models.FloatField()
    height = models.FloatField()
    TPV_photo = models.CharField(max_length=50, blank=True, default="-")
    UF_photo = models.CharField(max_length=50, blank=True, default="-")
    photo = models.CharField(max_length=50, blank=True, default="-")
    v_defects = models.CharField(max_length=10000, blank=True, default="-")
    u_defects = models.CharField(max_length=100, blank=True, default="-")
    code_support_in_1C = models.CharField(max_length=200, blank=True, default="-")
    guid = models.CharField(max_length=100, blank=True, default="-")
    flag_defects = models.BooleanField()
    comment_in_TOiR = models.CharField(max_length=100, blank=True, default="-")

class Feature(models.Model):
    type = models.CharField(max_length=100, blank=True, default="Feature")
    properties = models.OneToOneField(Tower, on_delete=models.CASCADE)
    geometry = models.OneToOneField(Geometry, on_delete=models.CASCADE)