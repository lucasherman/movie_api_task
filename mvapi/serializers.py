from .models import Movie, Comment
from rest_framework.serializers import ModelSerializer


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
