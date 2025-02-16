from urllib import request

from django.http import HttpResponse
from django.views.generic import DetailView, ListView

from goods.utils import q_search
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from goods.models import Product

class CatalogView(ListView):
    model = Product
    # queryset = Products.objects.all().order_by("-id")
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 8
    allow_empty = False # Означает что нельзя отображать пустую страницу, будет отображаться 404

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        grower_slug = self.kwargs.get('grower_slug')
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')

        if category_slug == 'all':
            #goods = Product.objects.all() # Поскольку указана model = Product
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            #goods = Product.objects.filter(category__slug=category_slug)
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404() # Обрабатываем случай когда querry-set со списком товаров пустой

        if grower_slug:
            goods = super().get_queryset().filter(grower__slug=grower_slug)

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Seed Shop - Каталог'
        context['category_slug'] = self.kwargs.get('category_slug')
        context['grower_slug'] = self.kwargs.get('grower_slug')
        return context


class ProductView(DetailView):
    # model = Product
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product" # имя контекстной переменной которую вернул get_object

    def get_object(self, queryset = None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(Product, slug=slug)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["title"] = self.object.name
            context["previous_url"] = self.request.META.get("HTTP_REFERER", '/')
            return context

# def catalog(request, category_slug=None) -> HttpResponse:
#     page = request.GET.get('page', 1) # Номер страницы, запрашиваемый пользователем
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)
#
#     if category_slug == 'all':
#         goods = Product.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = Product.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404() # Обрабатываем случай когда querry-set со списком товаров пустой
#
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#
#     if order_by and order_by != 'default':
#         goods = goods.order_by(order_by)
#
#     paginator = Paginator(goods, 8) # Будет показывать по 8 товаров
#     current_page = paginator.page(int(page))
#
#
#     context: dict[str, str] = {
#         'title': 'Каталог',
#         'goods': current_page,
#         'slug_url': category_slug,
#     }
#
#     return render(request, 'goods/catalog.html', context=context)


# def product(request, product_slug) -> HttpResponse:
#     product = Product.objects.get(slug=product_slug) # создание обьекта продукта
#     previous_url = request.META.get('HTTP_REFERER', '/') # создание url муршрута для перехода на прошлую страницу
#     category_slug = product.category.slug
#
#     context: dict = {
#         'title': f"Товар-{product.name}",
#         'previous_url': previous_url,
#         'product': product,
#         'category_slug': product_slug
#     }
#
#     return render(request, 'goods/product.html', context)