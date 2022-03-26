from pipes import Template
from re import template
from unicodedata import name
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .models import Dog

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

# class Dog:
#     def __init__(self, name, img, age, gender):
#         self.name = name
#         self.img = img
#         self.age = age
#         self.gender = gender

class DogList(TemplateView):
    template_name = 'doglist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["dogs"] = Dog.objects.filter(name__icontains=name) #add a key into the context object for view
            context["header"] = f"Searching for {name}"
        else:
            context["dogs"] = Dog.objects.all() #add a key into the context object for view
            context["header"] = "Our Cats"
        return context



