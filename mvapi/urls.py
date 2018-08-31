from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .views import MovieViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls')),
]