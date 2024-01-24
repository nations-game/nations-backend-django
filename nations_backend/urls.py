"""
URL configuration for nations_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import (
    signup_user,
    login_user,
    user_info,

    create_nation,
    nation_info
)

urlpatterns = [
    path("user/signup", signup_user, name="signup"),
    path("user/login", login_user, name="login"),
    path("user/info", user_info, name="info"),

    path("nation/create", create_nation, name="create_nation"),
    path("nation/info", nation_info, name="nation_info"),
    path("admin/", admin.site.urls),
]
