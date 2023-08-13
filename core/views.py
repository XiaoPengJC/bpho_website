from django.shortcuts import render
from django.http import HttpResponse
from .models import Planet
'''
import os
#from .utils import get_plot
import sys
current = os.path.dirname(os.path.realpath('bpho2023_main'))
sys.path.append(os.path.dirname(os.path.dirname(current)))
'''
from .bpho import *
import os.path
from .cache import Cache

planets = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
planet_list = []

# Create your views here.
def index(request):
    return render(request, 'index.html')

def task_1(request):
    context = {}

    imgdata = task1()

    context["svg_graph"] = imgdata

    return render(request, 'task_1.html', context)

def task_2(request):
    context = {}
    is_3D_orbit = False

    if request.GET:
        planets = [k.capitalize() for k, v in dict(request.GET).items() if v == ['on']]
        
        if "Is_3d_orbit" in planets:
            is_3D_orbit = True
            del planets[planets.index("Is_3d_orbit")]

        figure = task2(planets, is_3D_orbit)
        context["svg_graph"] = figure

    return render(request, 'task_2.html', context)

def task_3(request):
    context = {}

    if request.GET:
        planets = [k.capitalize() for k, v in dict(request.GET).items() if v == ['on']]

        imgdata = task3(planets)

        context["anim_graph"] = imgdata

    return render(request, 'task_3.html', context)

def task_4(request):
    context = {}

    if request.GET:
        planets = [k.capitalize() for k, v in dict(request.GET).items() if v == ['on']]

        imgdata = task4(planets)

        context["anim_graph"] = imgdata

    return render(request, 'task_4.html', context)

def task_5(request):
    context = {}

    imgdata = task5("Pluto")

    context["svg_graph"] = imgdata

    return render(request, 'task_5.html', context)

def task_6(request):
    context = {}

    if request.GET:
        planets = [k.capitalize() for k, v in dict(request.GET).items() if v == ['on']]

        imgdata = task6(planets)

        context["svg_graph"] = imgdata

    return render(request, 'task_6.html', context)

def task_7(request):
    context = {}
    is_3D_orbit = False

    if request.GET:
        planets = [k.capitalize() for k, v in dict(request.GET).items() if v == ['on']]
        try:
            centre = dict(request.GET)["planet"][0].capitalize()
        except:
            centre = "Earth"

        if "Is_3d_orbit" in planets:
            is_3D_orbit = True
            del planets[planets.index("Is_3d_orbit")]

        imgdata = task7A(centre, planets, is_3D_orbit)

        context["svg_graph"] = imgdata

    return render(request, 'task_7.html', context)