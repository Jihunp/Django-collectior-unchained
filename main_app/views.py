from unicodedata import name
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Dog, DogToy
from django.views.generic import DetailView
from django.urls import is_valid_path, reverse
from django.contrib.auth.models import User
# imports for Authentification
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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

@method_decorator(login_required, name='dispatch')
class Dog_Create(CreateView):
    model = Dog
    fields = ['name', 'img', 'age', 'gender', 'dogtoys']
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

@method_decorator(login_required, name='dispatch')
class Dog_Update(UpdateView):
    model = Dog
    fields = ['name', 'img', 'age', 'gender', 'dogtoys']
    template_name = "dog_update.html"
    # success_url = "/dogs"
    def get_success_url(self):
        return reverse('dog_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class Dog_Delete(DeleteView):
    model = Dog
    template_name = "dog_delete_confirmation.html"
    success_url = "/dogs/"

def profile(request, username):
    user = User.objects.get(username=username)
    dogs = Dog.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'dogs': dogs})


def dogtoys_index(request):
    dogtoys = DogToy.objects.all()
    return render(request, 'dogtoy_index.html', {'dogtoys': dogtoys})

def dogtoys_show(request, dogtoy_id):
    dogtoy = DogToy.objects.get(id=dogtoy_id)
    return render(request, 'dogtoy_show.html', {'dogtoy': dogtoy})

@method_decorator(login_required, name='dispatch')
class DogToyCreate(CreateView):
    model = DogToy
    fields = '__all__'
    template_name = "dogtoy_form.html"
    success_url = '/dogtoys'

@method_decorator(login_required, name='dispatch')
class DogToyUpdate(UpdateView):
    model = DogToy
    fields = ['name', 'color']
    template_name = "dogtoy_update.html"
    success_url = '/dogtoys'

@method_decorator(login_required, name='dispatch')
class DogToyDelete(DeleteView):
    model = DogToy
    template_name = "dogtoy_confirm_delete.html"
    success_url = '/dogtoys'

# login, logout, and signup
def login_view(request):
    # if POST, then user is authenticated
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            use = form.cleaned_data['username']
            pas = form.cleaned_data['password']
            user = authenticate(username = use, password = pas)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+use)
                else:
                    print('The account has been disabled')
                    # can redirect users here
            else:
                print('Username and/or password is incorrect')
    else:
        # user goes to login page
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/dogs')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('Hey', user.username)
            return HttpResponseRedirect('/user/'+str(user.username))
        else:
            HttpResponse('<h1>Please Try Again</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})