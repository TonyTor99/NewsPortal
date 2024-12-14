from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('cat_name',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('news_article', 'title', 'text')
