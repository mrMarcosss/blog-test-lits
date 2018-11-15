import random

from django.db.models import Prefetch
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from categories.models import Category
from posts.models import Post


class CategoriesListView(ListView):
    template_name = 'categories/categories_list.html'
    context_object_name = 'categories'
    queryset = Category.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['main_page'] = True
        return context


class CategoryDetailView(DetailView):
    template_name = 'categories/category_single.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['posts'] = True
        return context

    def get_queryset(self):
        return Category.objects.filter(slug=self.kwargs['slug']).prefetch_related(
            Prefetch(
                'posts', queryset=Post.objects.filter(is_active=True).select_related('user'), to_attr='category_posts'
            )
        )


def random_category(request):
    slugs = Category.objects.filter(is_active=True).values_list('slug', flat=True)
    return redirect('categories:category', slug=random.choice(slugs))


def random_post(request):
    slugs = Post.objects.filter(is_active=True).values_list('slug', flat=True)
    random_post = get_object_or_404(Post.objects.select_related('category'), slug=random.choice(slugs))
    return redirect('posts:post', category_slug=random_post.category.slug, slug=random_post.slug)
