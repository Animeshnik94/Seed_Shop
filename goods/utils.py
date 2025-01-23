from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Q

from goods.models import Product

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