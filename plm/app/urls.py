from django.urls import re_path
from app import views

urlpatterns = [
    re_path(r'^tower$', views.TowerAPI),
    re_path(r'^tower/([0-9]+)$', views.TowerAPI),
    re_path(r'^tower/upload$', views.FileUploadView.as_view())
]
