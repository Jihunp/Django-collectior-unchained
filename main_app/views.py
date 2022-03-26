from re import template
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView

# Create your views here.

class Home(View):
    def get(self, request):
        return HttpResponse("Dogs Home")

    class About(View):
        def get(self, request):
            return HttpResponse("About Dogs")

class Home(TemplateView):
    template_name= "home.html"

class About(TemplateView):
    template_name= "about.html"

class Dog:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

class DogList(TemplateView):
    template_name = 'doglist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dogs"] = dogs #add a key into the context object for view
        return context

dogs = [
    Dog("woof", 5, "male"),
    Dog("arf", 2, "female"),
    Dog("power", 45, "female"),
    Dog("drive", 423, "male"),
]

