import requests, inflection
from django.conf import settings


def retrieve_movie_data(title):
    response = requests.get('http://www.omdbapi.com/?t=' + title + '&plot=full&apikey=' + settings.OMDB_API_KEY)
    return {inflection.underscore(key): value for key, value in response.json().items()}
