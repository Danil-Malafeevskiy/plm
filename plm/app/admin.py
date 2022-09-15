from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Feature)
admin.site.register(Type)
admin.site.register(User, UserAdmin)
admin.site.register(VersionControl)