from django.urls import path
from goods import views

app_name = 'goods'

#namespace = catalog

urlpatterns = [
    # View - catalog
    #path('', views.catalog, name='index'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'), # Я использовал разный name для избежания проблем с url адресацией
    path('search/', views.CatalogView.as_view(), name='search'),
    # path('grower/<slug:grower_slug>/', views.grower, name='grower'),
    # View - product
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
]