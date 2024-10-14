from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    rating_author = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rate = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating_post'), 0))['pr']
        com_rate = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating_comm'), 0))['cr']
        post_com_rate = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating_comm'), 0))['pcr']

        self.rating_author = (post_rate * 3) + com_rate + post_com_rate
        self.save()


class Category(models.Model):
    cat_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.cat_name


class Post(models.Model):

    news = 'NE'
    article = 'AR'

    N_A = [
        (news, 'Новости'),
        (article, 'Статья')
    ]

    news_article = models.CharField(max_length=2,
                                    choices=N_A,
                                    default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating_post = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + '...'
        return self.text

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text_comm = models.TextField()
    time_comm = models.DateTimeField(auto_now_add=True)
    rating_comm = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comm += 1
        self.save()

    def dislike(self):
        self.rating_comm -= 1
        self.save()
