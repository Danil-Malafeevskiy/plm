from django.urls import re_path, include, path
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
    re_path(r'^dataset$',views.TypeView.as_view()),
    re_path(r'^dataset/([0-9]+)$',views.TypeView.as_view()),
    re_path(r'^dataset/admin/([0-9]+)$',views.TypeAdminView.as_view()),
    re_path(r'^dataset/admin$',views.TypeAdminView.as_view()),
    re_path(r'^version$', views.VersionControlView.as_view()),
    re_path(r'^version/([0-9]+)$', views.VersionControlView.as_view()),
    re_path(r'^password-reset', views.RequestResetPassword.as_view()),
    path('password-reset/<uidb64>/<token>', views.RequestResetPassword.as_view(), name='password-reset')
]
