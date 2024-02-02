"""
URL configuration for nations_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path, include

from .views import (
    # User views
    signup_user,
    login_user,
    user_info,
    get_notifications,
    read_notification,

    # Nation views
    create_nation,
    nation_info,
    nation_factories,
    collect_taxes,

    # Fatory views
    get_all_factories,
    build_factory,
    collect_from_factory,

    # Alliance view
    get_alliance_list,
    create_alliance,
    post_alliance_shout,
    get_join_requests,
    join_alliance,
    get_alliance_by_id,
)

urlpatterns = [
    path("api/", include([
        path("user/", include([
            path("signup", signup_user, name="signup"),
            path("login", login_user, name="login"),
            path("@<str:username>/info", user_info, name="info"),
            path("notifications", get_notifications, name="get_notifications"),
            path("readnotification", read_notification, name="read_notification"),
        ])),
        
        path("nation/", include([
            path("create", create_nation, name="create_nation"),
            path("info", nation_info, name="nation_info"),
            path("factories", nation_factories, name="nation_factories"),
            path("collecttaxes", collect_taxes, name="collect_taxes")
        ])),

        path("factories/", include([
            path("all", get_all_factories, name="get_all_factories"),
            path("build", build_factory, name="build_factory"),
            path("collect", collect_from_factory, name="collect_from_factory")
        ])),

        path("alliance/", include([
            path("list", get_alliance_list, name="get_alliance_list"),
            path("create", create_alliance, name="create_alliance"),
            path("join", join_alliance, name="join_alliance"),
            path("get", get_alliance_by_id, name="get_alliance_by_id"),

            path("admin/", include([
                path("shout", post_alliance_shout, name="post_alliance_shout"),
                path("joinrequests", get_join_requests, name="get_join_requests")
            ]))
        ]))
    ])),

    path("admin/", admin.site.urls),
]
