from django.urls import path

from .views import CategoriesListView, CategoryDetailView, random_category

app_name = 'categories'

urlpatterns = [
    path('', CategoriesListView.as_view(), name='categories'),
    path('category/random/', random_category, name='category_random'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
]
