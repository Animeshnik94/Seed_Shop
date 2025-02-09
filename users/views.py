from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from orders.models import Order, OrderItem
from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm

def login(request) -> HttpResponse:
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if session_key: # update добавляет в БД корзины после логина
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'): #Если неавторизованый пользователь решит перейти сразу в профиль, его перекинет на
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

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:  # update добавляет в БД корзины после логина
                Cart.objects.filter(session_key=session_key).update(user=user)

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

    orders = (Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("product"),
        )
    ).order_by("-id")
    )

    context = {
        'title': 'Seed Shop - Кабинет',
        'form': form,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context=context)

def users_cart(request):
    context = {
        'title': f'Корзина {request.user.username}',
    }
    return render(request, 'users/users_cart.html', context=context)
@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))

