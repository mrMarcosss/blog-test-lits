from django import template
from categories.models import Category

register = template.Library()


@register.inclusion_tag('categories/categories_dropdown.html')
def show_categories(category_id):
    data = {'categories': Category.objects.filter(is_active=True), 'active_category': category_id}
    return data
