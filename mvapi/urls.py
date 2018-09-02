from django.conf.urls import include, url
from .views import MovieList, CommentList

urlpatterns = [
    url(r'^api/', include('rest_framework.urls')),
    url(r'^movies/$', MovieList.as_view()),
    url(r'^comments/$', CommentList.as_view())
]