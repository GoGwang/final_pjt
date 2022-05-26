from tabnanny import verbose
# from unicodedata import category
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/community/tag/{self.slug}/'
    



class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/community/category/{self.slug}/'
    
    class Meta:
        verbose_name_plural = 'Categories'
    


class Review(models.Model):
    title = models.CharField(max_length=100)
    head_image = models.ImageField(upload_to='community/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='community/files/%Y/%m/%d/', blank=True)
    # movie_title = models.CharField(max_length=50)
    # rank = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    category = models.ForeignKey(Category, null= True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/community/{self.pk}/'
    
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.user}::{self.content}'

    def get_absolute_url(self):
        return f'{self.review.get_absolute_url()}#comment-{self.pk}'
    





