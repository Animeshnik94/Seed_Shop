from django.views.generic import TemplateView
from goods.utils import get_popular_products, get_new_products, get_powerful_products
from goods.models import Product



class IndexView(TemplateView):
    template_name = 'main/index.html'

    # def get(self, request, *args, **kwargs):
    #     print('123')
    #     return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Seed Shop - Главная'
        context['popular_products'] = get_popular_products(limit=8)
        context['new_products'] = get_new_products(limit=8)
        context['powerful_products'] = get_powerful_products(limit=8)

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