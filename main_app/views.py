from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Dog
from django.views.generic import DetailView
from django.urls import reverse
from django.contrib.auth.models import User

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

class Dog_Create(CreateView):
    model = Dog
    fields = ['name', 'img', 'age', 'gender']
    template_name = 'dog_create.html'
    # success_url = '/dogs/'
    def get_success_url(self):
        return reverse('dog_detail', kwarges={'pk': self.object.pk})
    
    def form_valid(self, form):
        self.object = form.save(commit= False)
        self.object.user = self.requset.user
        self.object.save()
        return HttpResponseRedirect('/dogs')


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

def profile(request, username):
    user = User.objects.get(username=username)
    dogs = Dog.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'dogs': dogs})