from django.urls import path
from main import views

app_name = 'main'

#namespace = main

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about_us/', views.AboutView.as_view(), name='about_us'),
]
