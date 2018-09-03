from django.db import models


class Movie(models.Model):

    title = models.CharField(max_length=250)
    year = models.CharField(max_length=4, null=True)
    rated = models.CharField(max_length=10, null=True)
    released = models.CharField(max_length=20, null=True)
    runtime = models.CharField(max_length=10, null=True)
    genre = models.CharField(max_length=100, null=True)
    director = models.CharField(max_length=250, null=True)
    writer = models.CharField(max_length=250, null=True)
    actors = models.CharField(max_length=500, null=True)
    plot = models.TextField(null=True)
    language = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    awards = models.TextField(null=True)
    poster = models.URLField(null=True)
    ratings = models.TextField(null=True)
    metascore = models.CharField(max_length=10, null=True)
    imdb_rating = models.CharField(max_length=10, null=True)
    imdb_votes = models.CharField(max_length=10, null=True)
    imdb_id = models.CharField(max_length=10, null=True, unique=True)
    type = models.CharField(max_length=20, null=True)
    dvd = models.CharField(max_length=20, null=True)
    box_office = models.CharField(max_length=20, null=True)
    production = models.CharField(max_length=100, null=True)
    website = models.URLField(max_length=100, null=True)
    response = models.CharField(max_length=100, null=True)


class Comment(models.Model):

    movie = models.ForeignKey(Movie, on_delete="cascade")
    body = models.TextField(null=True)
