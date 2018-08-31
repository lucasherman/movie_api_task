from .models import Movie, Comment
from rest_framework.viewsets import ModelViewSet
from .serializers import MovieSerializer, CommentSerializer


class MovieViewSet(ModelViewSet):

    queryset = Movie.objects.all().order_by('pk')
    serializer_class = MovieSerializer


class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all().order_by('pk')
    serializer_class = CommentSerializer
