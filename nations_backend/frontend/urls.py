from django.urls import path
from . import views

app_name = "frontend"

urlpatterns = [
    path("register/", views.signup, name="register"),
    path("login/", views.user_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("createnation/", views.create_nation, name="createnation"),
]
