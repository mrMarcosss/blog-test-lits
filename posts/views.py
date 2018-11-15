from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, ListView, UpdateView, CreateView, DeleteView
from posts.forms import PostEditForm
from posts.models import Post


class PostDetailView(DetailView):
    template_name = 'posts/post_single.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        filters = {'slug': self.kwargs['slug']}
        if self.request.user.is_authenticated and Post.objects.filter(
                slug=self.kwargs['slug'], user=self.request.user
        ).exists():
            filters['user'] = self.request.user
        else:
            filters['is_active'] = True
        return get_object_or_404(Post.objects.select_related('category'), **filters)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['others'] = Post.objects.filter(is_active=True).exclude(slug=self.kwargs['slug'])[:3]
        return context


@method_decorator(login_required, name='dispatch')
class UserPostsListView(ListView):
    context_object_name = 'posts'
    template_name = 'posts/my_posts.html'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).select_related('category')


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    form_class = PostEditForm

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).select_related('category')

    def get_success_url(self):
        return reverse_lazy('posts:post_edit', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Post saved successfully')
        return super(PostUpdateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    form_class = PostEditForm
    template_name = 'posts/post_form.html'

    def get_success_url(self):
        return reverse_lazy('posts:my_posts')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        messages.success(self.request, 'Post created successfully')
        return super(PostCreateView, self).form_valid(form)


class PostDeleteView(DeleteView):
    model = Post

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully')
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('posts:my_posts')


class SearchPosts(TemplateView):
    template_name = 'posts/search.html'

    def get_search_result(self, request):
        q = request.GET.get('q')
        if q:
            return Post.objects.filter(is_active=True).filter(Q(name__icontains=q) | Q(text__icontains=q))
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super(SearchPosts, self).get_context_data(**kwargs)
        context['result'] = self.get_search_result(self.request)
        context['q'] = self.request.GET.get('q')
        return context
