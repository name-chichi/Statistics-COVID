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

def openingclosing(request):
	context = {
		'section': 'openingclosing.html'
	}
	return render(request, 'index.html', context)

def openingclosings(request):
	data = Restaurant().OpeningClosing()
	return HttpResponse(json.dumps(data), content_type='application/json')

def region(request):
	context = {
		'section': 'region.html'
	}
	return render(request, 'index.html', context)

def regions(request):
	return