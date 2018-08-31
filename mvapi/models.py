from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

YEARS = list(range(1921, (datetime.now().year+1)))
YEAR_CHOICES = zip(map(str, YEARS), YEARS)



class Movie(models.Model):

    title = models.CharField(max_length=250)
    year = models.IntegerField(choices=YEAR_CHOICES, null=True)
    rated = models.CharField(max_length=10,null=True)
    released = models.DateField(null=True)
    runtime = models.IntegerField(null=True)
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
    metascore = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)
    imdbrating = models.DecimalField\
            (
                validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
                null=True,
                decimal_places=1,
                max_digits=3
            )
    imdbvotes = models.IntegerField(validators=[MinValueValidator(0.0)], null=True)
    imdbid = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=20, null=True)
    dvd = models.DateField(null=True)
    boxoffice = models.CharField(max_length=10, null=True)
    production = models.CharField(max_length=100, null=True)
    website = models.URLField(null=True)
    response = models.NullBooleanField(null=True)


class Comment(models.Model):

    movie = models.ForeignKey(Movie, on_delete="cascade")
    body = models.TextField(null=True)



