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
import django.contrib.auth.urls

from .views import (
    # Misc views
    tick_nations,
    
    # User views
    signup_user,
    login_user,
    user_info,
    get_notifications,
    read_notification,
    get_message,
    get_inbox,
    send_message,
    get_sent_messages,

    # Nation views
    create_nation,
    nation_info,
    nation_factories,
    collect_taxes,
    nation_buildings,
    get_nation_by_id,
    upgrade,
    upgrades,

    # Factory views
    get_all_factories,
    build_factory,
    collect_from_factory,

    # Alliance views
    get_alliance_list,
    get_alliance_list_pagination,
    create_alliance,
    post_alliance_shout,
    get_join_requests,
    join_alliance,
    get_alliance_by_id,
    get_alliance_members,
    leave_alliance,
    accept_join_request,
    delete_alliance,
    transfer_ownership,
    kick_member,
    promote_member,
    demote_member,
    get_alliance_relations,
    get_ally_requests,
    deny_ally_request,
    accept_ally_request,
    declare_enemy,
    send_ally_request,

    # Buildings views
    get_all_buildings,
    build_building,

    # Military Views,
    get_all_units,
    nation_divisions,
    add_division,
    recruit_unit,
    move_unit,
)

urlpatterns = [
    path("api/", include([
        path("tick", tick_nations, name="tick_nations"),

        path("user/", include([
            path("signup", signup_user, name="signup"),
            path("login", login_user, name="login"),
            path("@<str:username>/info", user_info, name="info"),
            path("notifications", get_notifications, name="get_notifications"),
            path("readnotification", read_notification, name="read_notification"),
            path("getmessage", get_message, name="get_message"),
            path("sendmessage", send_message, name="send_message"),
            path("inbox", get_inbox, name="inbox"),
            path("sentmessages", get_sent_messages, name="get_sent_messages"),
        ])),
        
        path("nation/", include([
            path("create", create_nation, name="create_nation"),
            path("info", nation_info, name="nation_info"),
            path("factories", nation_factories, name="nation_factories"),
            path("collecttaxes", collect_taxes, name="collect_taxes"),
            path("buildings", nation_buildings, name="nation_buildings"),
            path("get", get_nation_by_id, name="get_nation_by_id"),
            path("upgrade", upgrade, name="upgrade"),
            path("upgrades", upgrades, name="upgrades")
        ])),

        path("factories/", include([
            path("all", get_all_factories, name="get_all_factories"),
            path("build/", build_factory, name="build_factory"),
            path("collect", collect_from_factory, name="collect_from_factory")
        ])),

        path("alliance/", include([
            path("list", get_alliance_list, name="get_alliance_list"),
            path("list_page", get_alliance_list_pagination, name="get_alliance_list_page"),
            path("create", create_alliance, name="create_alliance"),
            path("join", join_alliance, name="join_alliance"),
            path("get", get_alliance_by_id, name="get_alliance_by_id"),
            path("members", get_alliance_members, name="get_alliance_members"),
            path("leave", leave_alliance, name="leave_alliance"),
            path("getrelations", get_alliance_relations, name="get_alliance_relations"),

            path("admin/", include([
                path("shout", post_alliance_shout, name="post_alliance_shout"),
                path("joinrequests", get_join_requests, name="get_join_requests"),
                path("acceptrequest", accept_join_request, name="accept_join_request"),
                path("delete", delete_alliance, name="delete_alliance"),
                path("promote", promote_member, name="promote_member"),
                path("kick", kick_member, name="kick_member"),
                path("transfer", transfer_ownership, name="transfer_ownership"),
                path("demote", demote_member, name="demote_member"),
                path("getallyrequests", get_ally_requests, name="get_ally_requests"),
                path("denyallyrequest", deny_ally_request, name="deny_ally_request"),
                path("acceptallyrequest", accept_ally_request, name="acceptallyrequest"),
                path("declareenemy", declare_enemy, name="declare_enemy"),
                path("sendallyrequest", send_ally_request, name="send_ally_request"),
            ]))
        ])),

        path("buildings/", include([
            path("all", get_all_buildings, name="get_all_buildings"),
            path("build/", build_building, name="build_building"),
        ])),

        path("military/", include([
            path("allUnits", get_all_units, name="get_all_units"),
            path("divisions", nation_divisions, name="nation_divisions"),
            path("addDivision", add_division, name="add_division"),
            path("recruitUnit", recruit_unit, name="recruit_unit"),
            path("moveUnit", move_unit, name="move_unit"),
        ]))
    ])),

    path("admin/", admin.site.urls),
    path("app/", include("nations_backend.frontend.urls")),
]
