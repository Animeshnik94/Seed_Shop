from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView

from common.mixins import CacheMixin
from goods.models import Product
from orders.models import Order, OrderItem
from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    #success_url = reverse_lazy('main:index')

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page          #Если неавторизованый пользователь решит перейти сразу в профиль, его перекинет на
        return reverse_lazy('main:index') # страницу авторизации, после авторизации на его страницу

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Seed Shop - Авторизация'
        return context

class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, Вы успешно зарегистрировались и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Seed Shop - Регистрация'
        return context

class UserProfileView(LoginRequiredMixin, CacheMixin,UpdateView): # Login Required Mixin нужен для того
                                                                  # чтобы мог зайти только авторизованый юзер
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset = None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Seed Shop - Кабинет'

        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product")
            )
        ).order_by("-id")

        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60 * 2)
        return context

class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Seed Shop - Корзина'
        context['products'] = Product.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
        auth.logout(request)
        return redirect(reverse('main:index'))

# @login_required
# def logout(request):
#     messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
#     auth.logout(request)
#     return redirect(reverse('main:index'))

# def users_cart(request):
#     context = {
#         'title': f'Корзина {request.user.username}',
#     }
#     return render(request, 'users/users_cart.html', context=context)

# @login_required #Этот декоратор перекинет тебя на страницу авторизации
# def profile(request) -> HttpResponse:
#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Профиль успешно обновлен")
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = ProfileForm(instance=request.user)
#
#     orders = (Order.objects.filter(user=request.user).prefetch_related(
#         Prefetch(
#             "orderitem_set",
#             queryset=OrderItem.objects.select_related("product"),
#         )
#     ).order_by("-id")
#     )
#
#     context = {
#         'title': 'Seed Shop - Кабинет',
#         'form': form,
#         'orders': orders,
#     }
#     return render(request, 'users/profile.html', context=context)



# def login(request) -> HttpResponse:
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#
#             session_key = request.session.session_key
#
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, Вы вошли в аккаунт")
#
#                 if session_key: # update добавляет в БД корзины после логина
#                     # delete old authorized user carts
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     # add new authorized user carts from anonimous session
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#
#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'): #Если неавторизованый пользователь решит перейти сразу в профиль, его перекинет на
#                     return HttpResponseRedirect(request.POST.get('next')) # страницу авторизации, после авторизации на его страницу
#
#                 return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'title': 'Seed Shop - Авторизация',
#         'form': form,
#     }
#     return render(request, 'users/login.html', context=context)


# def registration(request) -> HttpResponse:
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#
#             session_key = request.session.session_key
#
#             user = form.instance
#             auth.login(request, user)
#
#             if session_key:  # update добавляет в БД корзины после логина
#                 Cart.objects.filter(session_key=session_key).update(user=user)
#
#             messages.success(request, f"{user.username}, Вы успешно зарегестрированы и вошли в аккаунт")
#             return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserRegistrationForm()
#
#     context = {
#         'title': 'Seed Shop - Регистрация',
#         'form': form,
#     }
#     return render(request, 'users/registration.html', context=context)