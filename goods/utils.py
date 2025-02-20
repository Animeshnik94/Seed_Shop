from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from orders.models import OrderItem
from django.db.models import Count
#from django.db.models import Q

from goods.models import Product

#--------- Список популярных товаров --------
def get_popular_products(limit=8):
    """
    Возвращает список самых популярных товаров.
    :param limit: Количество товаров (по умолчанию 8).
    :return: QuerySet популярных товаров.
    """
    popular_products = OrderItem.objects.values('product').annotate(total_sold=Count('product')).order_by(
        '-total_sold')[:limit]  # Возвращает <QuerySet [{'product': 1, 'total_sold': 10},
                                # {'product': 3, 'total_sold': 8},
                                # {'product': 2, 'total_sold': 5}, ...]>

    # Возвращает список id популярных товаров
    popular_product_ids = [item['product'] for item in popular_products]
    # Создает список из популярных товаров по их id
    popular_products_list = Product.objects.filter(id__in=popular_product_ids)

    return popular_products_list

#---------- Список новых товаров ---------
def get_new_products(limit=8):
    """
    Возвращает список новых товаров.
    :param limit: Количество товаров (по умолчанию 8).
    :return: QuerySet новых товаров.
    """
    new_products = Product.objects.order_by('date_added')[:limit]

    return new_products

def q_search(query): # Функция необходима для поиска товара через форму поиска
    if query.isdigit() and len(query) <= 5: 
        return Product.objects.filter(id=int(query)) # возвращает товары по id

    vector = SearchVector("name", "description")
    query = SearchQuery(query)
    
    result = (
        Product.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>"
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>"
        )
    )
    return result
    # keywords = [word for word in query.split() if len(word) > 2] # создает список из ключевых слов

    # q_objects = Q() # Создание Q-обьекта
    
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token) # Добавляет фильтрацию по описанию
    #     q_objects |= Q(name__icontains=token) # Добавляет фильтрацию по имени
    
    # return Product.objects.filter(q_objects) # Возвращает товары после фильтрации