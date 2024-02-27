from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm, NationCreateForm
from http import HTTPStatus
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from ..decorators import parse_json, needs_auth_frontend, needs_nation_frontend
from ..models import User, Nation
from ..buildings import building_manager
from ..factories import factory_manager

def signup(request: HttpRequest):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/app/dashboard")
    else:
        form = SignUpForm()
    return render(request, "signup.html", { "form": form })

def user_login(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/app/dashboard")
    else:
        form = LoginForm()
    return render(request, "login.html", { "form": form })

@needs_auth_frontend
def dashboard(request: HttpRequest):
    user: User = request.user
    if user.nation == None:
        return redirect("/app/createnation")
    
    info_dict =  {
        "user": request.user.to_dict(),  
        "nation": user.nation,
    }

    nation: Nation = user.nation

    factory_info_dict = {}

    for nation_factory in nation.get_factories():
        factory_type_id = nation_factory.factory_type
        factory_type_info = factory_manager.get_factory_by_id(factory_type_id).__dict__()
        ticks_run = nation_factory.ticks_run

        if factory_type_id not in factory_info_dict:
            factory_info_dict[factory_type_id] = {
                "info": factory_type_info,
                "ticks_run": ticks_run,
                "quantity": 1 
            }
        else:
            factory_info_dict[factory_type_id]["ticks_run"] += ticks_run
            factory_info_dict[factory_type_id]["quantity"] += 1

    factory_info_list = list(factory_info_dict.values())

    building_info_list = []

    for nation_building in nation.get_buildings():
        building_type_id = nation_building.building_type
        building_type_info = building_manager.get_building_by_id(building_type_id).__dict__()
        level = nation_building.level

        info_dict = building_type_info
        info_dict.update({ "level": level })
        building_info_list.append(info_dict)

    info_dict.update({
        "factories": factory_info_list,
        "buildings": building_info_list
    })
    
    return render(request, "dashboard.html", info_dict)

@needs_auth_frontend
def create_nation(request: HttpRequest):
    user: User = request.user
    if request.method == "POST":
        form = NationCreateForm(request.POST)
        if form.is_valid():
            # nation = form.save()
            nation: Nation = Nation.objects.create(
                name=form.data["name"],
                system=form.data["system"],
                leader=user
            )
            user.nation = nation
            user.save()
            return redirect("/app/dashboard") 
    else:
        form = NationCreateForm()
    return render(request, "create_nation.html", { "form": form })