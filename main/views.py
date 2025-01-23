from django.shortcuts import render
from django.http import HttpResponse

from goods.models import Category, Grower


def index(request) -> HttpResponse:
    context: dict[str, str] = {
        'title': 'Seed Shop - Главная', 
    }
    
    return render(request, 'main/index.html', context=context)

def about_us(request) -> HttpResponse:
    context: dict[str, str] = {
        'title': 'О нас',
    }
    return render(request, 'main/about.html', context)