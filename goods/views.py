from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from goods.utils import q_search

from goods.models import Product

def catalog(request, category_slug=None) -> HttpResponse:
    page_number = request.GET.get('page') # Номер страницы, запрашиваемый пользователем
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Product.objects.all()
    else:
        goods = Product.objects.filter(category__slug=category_slug)

    if query:
        goods = q_search(query)

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    if not goods.exists(): # Обрабатываем случай когда querry-set со списком товаров пустой
        goods = []

    paginator = Paginator(goods, 8) # Будет показывать по 8 товаров
    goods_page = paginator.get_page(page_number)

    context: dict[str, str] = {
        'title': 'Каталог',
        'goods': goods_page,
        'slug_url': category_slug,
    }

    return render(request, 'goods/catalog.html', context=context)

def product(request, product_slug) -> HttpResponse:
    product = Product.objects.get(slug=product_slug) # создание обьекта продукта
    previous_url = request.META.get('HTTP_REFERER', '/') # создание url муршрута для перехода на прошлую страницу
    category_slug = product.category.slug    

    context: dict = {
        'title': f"Товар-{product.name}",
        'previous_url': previous_url,
        'product': product,
        'category_slug': product_slug
    }

    return render(request, 'goods/product.html', context)