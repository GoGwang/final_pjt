from django.db import models
from accounts.models import User
from django.conf import settings
import os

class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    movie_like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='movie_like_reviews')
    genres = models.ManyToManyField(Genre)
    
    def get_absolute_url(self):
        return f'/{self.pk}/'

class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()

class Movie_Comment(models.Model):
    content = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # rate = models.floatrField(validators=[MinValueValidator(0.5),MaxValueValidator(5.0)], null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{ self.user}::{self.content}'

    def get_absolute_url(self):
        return f'{self.movie.get_absolute_url()}'

