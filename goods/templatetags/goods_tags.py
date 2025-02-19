from django import template
from urllib.parse import urlencode
from goods.models import Category, Product
from goods.models import Grower

register = template.Library()

@register.simple_tag()
def tag_categories():
    return Category.objects.all()

@register.simple_tag()
def tag_growers():
    return Grower.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)