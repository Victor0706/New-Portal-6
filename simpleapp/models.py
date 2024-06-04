from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

# Новость в списке
class New(models.Model):
    title = models.CharField(
        max_length=128,
        unique=True,  # названия новостей не должны повторяться
    )
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
    )
    # поле категории будет ссылаться на модель категории
    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='news', # все новости в категории будут доступны через поле news
    )
    category = models.TextField(default='new')
    added_at = models.DateTimeField(
        auto_now=True,
    )
    newAuthor = models.ManyToManyField('Author', through='NewAuthor')


    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])


class Article(models.Model):
    title = models.CharField(
        max_length=128,
        unique=True,
    )
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
    )

    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='articles',
    )
    category = models.TextField(default='article')
    added_at = models.DateTimeField(
        auto_now=True,
    )


    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )


class NewAuthor(models.Model):
    newThrough = models.ForeignKey(New, on_delete=models.CASCADE)
    authorThrough = models.ForeignKey(Author, on_delete=models.CASCADE)