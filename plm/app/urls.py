from django.urls import re_path, include
from app import views

urlpatterns = [
    re_path(r'^tower$', views.TowerAPI.as_view()),
    re_path(r'^tower/([0-9]+)$', views.TowerAPI.as_view()),
    re_path(r'^tower/upload$', views.FileUploadView.as_view()),
    re_path('tower/auth/', include('rest_framework.urls')),
    re_path(r'^tower/login$', views.LoginView.as_view()),
    re_path(r'^tower/logout$', views.LogoutView.as_view()),
    re_path(r'^group$', views.GroupView.as_view()),
    re_path(r'^group/([0-9]+)$', views.GroupView.as_view()),
    re_path(r'^user$', views.UserView.as_view()),
    re_path(r'^user/admin$',views.UserAdminView.as_view()),
    re_path(r'^user/admin/([0-9]+)$',views.UserAdminView.as_view()),
    re_path(r'^dataset$',views.DatasetView.as_view()),
    re_path(r'^dataset/([0-9]+)$',views.DatasetView.as_view()),
    re_path(r'^dataset/admin/([0-9]+)$',views.DatasetAdminView.as_view()),
    re_path(r'^dataset/admin$',views.DatasetAdminView.as_view()),
    re_path(r'^test$',views.room),
    re_path(r'^version$', views.VersionControlView.as_view()),
    re_path(r'^version/([0-9]+)$', views.VersionControlView.as_view()),
]
