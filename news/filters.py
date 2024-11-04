from django import forms
from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, ModelMultipleChoiceFilter, CharFilter

from .models import Post, Category


class PostFilter(FilterSet):
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

    # class Meta:
    #     model = Post
    #     fields = {
    #         'title': ['icontains']
    #     }
