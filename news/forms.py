from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]
