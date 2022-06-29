from django.db import models

class Tower(models.Model):
    Unique_number = models.IntegerField(unique=True)
    name_tap = models.CharField(max_length=50, default="")
    number_support = models.IntegerField(unique=True, default=id)
    VL = models.CharField(max_length=100, default="")
    type_support = models.CharField(max_length=50)
    code_support = models.CharField(max_length=50, default= "Не определен")
    material = models.CharField(max_length=50)
    corner = models.FloatField()
    X = models.FloatField()
    Y = models.FloatField()
    Z = models.FloatField()
    shirota = models.FloatField()
    dolgota = models.FloatField()
    height = models.FloatField()
    TPV_photo = models.CharField(max_length=50, default="")
    UF_photo = models.CharField(max_length=50, default="")
    photo = models.CharField(max_length=50, default="")
    v_defects = models.CharField(max_length=100, default="")
    u_defects = models.CharField(max_length=100, default="")
    code_support_in_1C = models.CharField(max_length=200, default="")
    guid = models.IntegerField(default=-1)
    flag_defects = models.BooleanField()
    comment_in_TOiR = models.CharField(max_length=100, default="")
    geometry = models.CharField(max_length=100, default="")