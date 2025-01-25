from django.shortcuts import render
from django.http import HttpResponse

def login(request) -> HttpResponse:
    context = {
        'title': 'Seed Shop - Авторизация',
    }
    return render(request, 'users/login.html', context=context)

def registration(request) -> HttpResponse:
    context = {
        'title': 'Seed Shop - Регистрация',
    }
    return render(request, 'users/registration.html', context=context)

def profile(request) -> HttpResponse:
    context = {
        'title': 'Seed Shop - Кабинет',
    }
    return render(request, 'users/profile.html', context=context)

def logout(request): pass