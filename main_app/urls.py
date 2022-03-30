from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('dogs/', views.DogList.as_view(), name="dog_list"),
    path('dogs/new/', views.Dog_Create.as_view(), name="dog_create"),
    path('dogs/<int:pk>/', views.Dog_Detail.as_view(), name="dog_detail"),
    path('dogs/<int:pk>/update', views.Dog_Update.as_view(), name="dog_update"),
    path('dogs/<int:pk>/delete', views.Dog_Delete.as_view(), name="dog_delete"),
    path('user/<username>/', views.profile, name="profile"),
]

