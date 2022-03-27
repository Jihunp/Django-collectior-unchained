from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('dogs/', views.DogList.as_view(), name="dog_list"),
    path('dogs/new/', views.Dog_Create.as_view(), name="cat_create"),
    path('dogs/<int:pk>/', views.DogDetail.as_view(), name="dog_detail"),
    path('dogs/<int:pk>/update', views.DogUpdate.as_view(), name="dog_update")
]

