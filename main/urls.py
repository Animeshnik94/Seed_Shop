from django.urls import path
from django.views.decorators.cache import cache_page

from main import views

app_name = 'main'

#namespace = main

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about_us/', cache_page(60)(views.AboutView.as_view()), name='about_us'),
    # кэширование целой страницы применяется редко,
    # куда уместнее применять кэширование локально
]
