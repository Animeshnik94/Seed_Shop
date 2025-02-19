from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Product
from orders.models import OrderItem


class IndexView(TemplateView):
    template_name = 'main/index.html'

    # def get(self, request, *args, **kwargs):
    #     print('123')
    #     return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Seed Shop - Главная'

        # Получаем топ-8 самых популярных товаров
        popular_products = OrderItem.objects.values('product').annotate(total_sold=Count('product')).order_by(
            '-total_sold')[:8] # Возвращает <QuerySet [{'product': 1, 'total_sold': 10},
                                                     # {'product': 3, 'total_sold': 8},
                                                     # {'product': 2, 'total_sold': 5}, ...]>
        # Возвращает список id популярных товаров
        popular_product_ids = [item['product'] for item in popular_products]
        # Создает список из популярных товаров по их id
        popular_products_list = Product.objects.filter(id__in=popular_product_ids)
        context['popular_products'] = popular_products_list

        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        context['username'] = self.request.user.username
        return context


# def index(request) -> HttpResponse:
#     context: dict[str, str] = {
#         'title': 'Seed Shop - Главная',
#     }
#
#     return render(request, 'main/index.html', context=context)

# def about_us(request) -> HttpResponse:
#     context: dict[str, str] = {
#         'title': 'О нас',
#     }
#     return render(request, 'main/about.html', context)