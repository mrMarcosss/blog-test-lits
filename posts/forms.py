from django import forms

from posts.models import Post


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'text', 'category', 'img_big', 'img_small', 'is_active')
