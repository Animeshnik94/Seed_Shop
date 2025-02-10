from django.http import HttpResponse
from django.core.paginator import Paginator
from goods.utils import q_search
from django.http import Http404
from django.shortcuts import render

from goods.models import Product

def catalog(request, category_slug=None) -> HttpResponse:
    page = request.GET.get('page', 1) # Номер страницы, запрашиваемый пользователем
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Product.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Product.objects.filter(category__slug=category_slug)
        if not goods.exists():
            raise Http404() # Обрабатываем случай когда querry-set со списком товаров пустой

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 8) # Будет показывать по 8 товаров
    current_page = paginator.page(int(page))


    context: dict[str, str] = {
        'title': 'Каталог',
        'goods': current_page,
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