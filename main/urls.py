from django.urls import path
from main import views

app_name = 'main'

#namespace = main

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
]
