from django.urls import path

from apps.user.views import (
    us_login,
    register,
    us_info,
    us_logout
)

app_name = 'user'

urlpatterns = [
    path("login/", us_login, name='login'),
    path("register/", register, name='register'),
    path("info/", us_info, name='info'),
    path("log-out/", us_logout, name='log-out')
]
