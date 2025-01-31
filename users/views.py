from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm

def login(request) -> HttpResponse:
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if request.POST.get('next', None): #Если неавторизованый пользователь решит перейти сразу в профиль, его перекинет на 
                    return HttpResponseRedirect(request.POST.get('next')) # страницу авторизации, после авторизации на его страницу

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
            messages.success(request, f"{user.username}, Вы успешно зарегестрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Seed Shop - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context=context)

@login_required #Этот декоратор перекинет тебя на страницу авторизации
def profile(request) -> HttpResponse:
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
    context = {
        'title': 'Seed Shop - Кабинет',
        'form': form,
    }
    return render(request, 'users/profile.html', context=context)

def users_cart(request):
    return render(request, 'users/users_cart.html')
@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))

