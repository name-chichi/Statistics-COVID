import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from analysis.food import Restaurant


def home(request):
	data = []
	context = {
		'section': 'main_section.html',
		'persons': data,
	}
	return render(request, 'index.html', context)

def dashboard1(request):
	context = {
		'section': 'dashboard1.html'
	}
	return render(request, 'index.html', context)

def dashboard2(request):
	context = {
		'section': 'dashboard2.html'
	}
	return render(request, 'index.html', context)

def dashboard3(request):
	context = {
		'section': 'dashboard3.html'
	}
	return render(request, 'index.html', context)

def openingclosing(request):
	context = {
		'section': 'openingclosing.html'
	}
	return render(request, 'index.html', context)

def openingclosings(request):
	data = Restaurant().OpeningClosing()
	return HttpResponse(json.dumps(data), content_type='application/json')
