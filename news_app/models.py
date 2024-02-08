from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.apps import AppConfig
from django.core.signals import setting_changed
from django.views.generic import UpdateView, DeleteView


class PublishedManager(models.Model):
    def get_queryset(self):
        return super().get_queryset().filter(status = News.Status.Published)
class Category(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class News(models.Model):

    class Status(models.TextChoices):
        Draft = 'DF','DRAFT'
        Published = 'PB','PUBLISHED'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    images = models.ImageField(upload_to='news/images')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    upgrade_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices, default=Status.Published)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish_time']
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail_page',args=[self.slug])
class Contacts(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email


class Comment(models.Model):
    news = models.ForeignKey(News,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')

    body = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['create_time']

    def __str__(self):
        return f'Comments  {self.body} by {self.user}'