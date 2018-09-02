from .models import Movie, Comment
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MovieSerializer, CommentSerializer
from .omdb_connector import retrieve_movie_data
from django.shortcuts import get_object_or_404


class MovieViewSet(ModelViewSet):

    queryset = Movie.objects.all().order_by('pk')
    serializer_class = MovieSerializer


class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all().order_by('pk')
    serializer_class = CommentSerializer


class MovieList(APIView):

    def get(self, request):
        movies = Movie.objects.all().order_by('pk')
        movies_serialized = MovieSerializer(movies, many=True)
        return Response(movies_serialized.data)

    def post(self, request):
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


class CommentList(APIView):

    def get(self, request):
        comments = Comment.objects.all()
        if(request.GET.get('movie_id')):
            comments = comments.filter(movie_id=request.GET.get('movie_id'))
        comments.order_by('pk')
        comments_serialized = CommentSerializer(comments, many=True)
        return Response(comments_serialized.data)

    def post(self, request):
        movie_id = request.POST.get('movie_id')
        if not movie_id:
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
