from django import forms
from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, ModelMultipleChoiceFilter, CharFilter, ChoiceFilter

from .models import Post, Category


class PostFilter(FilterSet):

    type = ChoiceFilter(
        field_name='news_article',
        choices=Post.N_A,
        required=False,
        empty_label='Все типы',
        label='Тип поста',
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Название'
    )

    added_after = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
        label='Опубликованы после'
    )

    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        to_field_name='id',
        widget=forms.CheckboxSelectMultiple,
        label='Категории'
    )

    class Meta:
        model = Post
        fields = ['title', 'added_after', 'category', 'news_article']
