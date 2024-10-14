from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
            'author',
        ]
