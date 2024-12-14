from django.contrib import admin
from .models import Author, Post, Category, Comment
from modeltranslation.admin import TranslationAdmin


class CategoryTranslationAdmin(TranslationAdmin):

    model = Category


class PostTranslationAdmin(TranslationAdmin):

    model = Post


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating_post=0)


nullfy_rating.short_description = 'Обнулить рейтинг поста'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'categories', 'news_article')
    list_filter = ('news_article', 'title', 'time_in', 'author', 'category')
    search_fields = ('title', 'text', 'category__cat_name')
    actions = [nullfy_rating]

    def categories(self, obj):
        return ', '.join([category.cat_name for category in obj.category.all()])


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
