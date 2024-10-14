import django_filters
from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        to_field_name='id',
        empty_label='любая категория'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains']
        }
