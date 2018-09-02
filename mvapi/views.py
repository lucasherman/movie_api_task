from .models import Movie, Comment
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MovieSerializer, CommentSerializer
from .omdb_connector import retrieve_movie_data
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class MovieList(generics.ListCreateAPIView):

    serializer_class = MovieSerializer
    queryset = Movie.objects.all().order_by('pk')
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_fields = ('title', 'year', 'director')
    ordering_fields = ('year', 'title')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        if title:
            movie_data = retrieve_movie_data(title)
            try:
                movie = Movie.objects.get(imdb_id=movie_data['imdb_id'])
                movie.__dict__.update(movie_data)
                movie.save()
                return Response(MovieSerializer(movie).data, status=status.HTTP_200_OK)
            except Movie.DoesNotExist:
                movie = Movie.objects.create(**movie_data)
                return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Title parameter not provided")


class CommentList(generics.ListCreateAPIView):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('pk')
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_fields = ('movie_id', )
    ordering_fields = ('movie_id', )

    def post(self, request, *args, **kwargs):
        movie_id = request.POST.get('movie_id')
        if movie_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Movie id not provided")

        movie = get_object_or_404(Movie, pk=movie_id)
        comment_body = request.POST.get('comment_body')
        if comment_body:
            comment = Comment()
            comment.movie = movie
            comment.body = comment_body
            comment.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Comment Body parameter is missing or empty")
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
