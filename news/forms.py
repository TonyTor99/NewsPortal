from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    title = forms.CharField(
        min_length=20,
        label='Название'
    )

    text = forms.CharField(
        min_length=20,
        label='Текст'
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Категории'
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]
