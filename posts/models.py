from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    name = models.CharField(max_length=250, unique=True)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ForeignKey('categories.Category', on_delete=models.PROTECT, related_name='posts')
    img_big = models.ImageField()
    img_small = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=False, db_index=True)

    def get_absolute_url(self):
        return reverse('posts:post', kwargs={'slug': self.slug, 'category_slug': self.category.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Post, self).save(*args, **kwargs)
