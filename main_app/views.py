from dataclasses import fields
from nis import cat
from pipes import Template
from re import template
from sre_constants import SUCCESS
from unicodedata import name
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Dog
from django.views.generic import DetailView
from django.urls import reverse

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
            context["header"] = "Our Dogs:"
        return context

class Dog_create(CreateView):
    model = Dog
    fields = ['name', 'img', 'age', 'gender']
    template_name = 'dog_create.html'
    # success_url = '/dogs/'
    def get_success_url(self):
        return reverse('dog_detail', kwarges={'pk': self.object.pk})

class Dog_Detail(DetailView):
    model = Dog
    template_name = "dog_detail.html"

class Dog_Update(UpdateView):
    model = Dog
    fields = ['name', 'img', 'age', 'gender']
    template_name = "dog_update.html"
    # success_url = "/dogs"
    def get_success_url(self):
        return reverse('dog_detail', kwargs={'pk': self.object.pk})

class Dog_Delete(DeleteView):
    model = Dog
    template_name = "dog_delete_confirmation.html"
    success_url = "/dogs/"