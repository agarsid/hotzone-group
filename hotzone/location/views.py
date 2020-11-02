from django.http import HttpResponse
from django.shortcuts import render
from .models import Locations
import requests
import json


def index(request):
    result = {'input': '', 'found': True, 'inDatabase': False}
    return render(request, 'location/index.html', result)


def search(request):
    loc = request.GET.get('query')
    res = requests.get('https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q={0}'.format(loc))
    try:
        res_json = json.loads(res.text)
    except:
        return render(request, 'location/notfound.html', {'input': loc, 'found': False})

    resp = res_json[0]
    name = resp['nameEN']
    address = resp['addressEN']
    x = resp['x']
    y = resp['y']
    result = {
        'input': loc,
        'name': name,
        'address': address,
        'x': x,
        'y': y,
    }
    return render(request, 'location/result.html', result)


def add(request):
    name = request.GET.get('name')
    address = request.GET.get('address')
    x = request.GET.get('x')
    y = request.GET.get('y')
    L = Locations(
        name=name, 
        address=address, 
        x_coord=x,
        y_coord=y)
    L.save()
    result = {'input': '', 'found': True, 'inDatabase': True}
    return render(request, 'location/added.html', result)