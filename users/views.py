from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from users.forms import UserLoginForm
from users.forms import UserRegistrationForm

def login(request) -> HttpResponse:
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Seed Shop - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context=context)

def registration(request) -> HttpResponse:
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Seed Shop - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context=context)

def profile(request) -> HttpResponse:
    context = {
        'title': 'Seed Shop - Кабинет',
    }
    return render(request, 'users/profile.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))