from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from .models import Movie, Comment
from .views import MovieList, CommentList

factory = APIRequestFactory()
movie_view = MovieList.as_view()
comment_view = CommentList.as_view()

class GetMovieTest(APITestCase):

    fixtures = ['fixtures.json']

    def test_get_movies(self):
        request = factory.get('/api/movies/')
        response = movie_view(request)
        movies_count = Movie.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movies_count, len(response.data))

    def test_get_movies_by_year(self):
        year = 2018
        request = factory.get('/api/movies?year=' + str(year))
        response = movie_view(request)
        movies_count = Movie.objects.filter(year=year).count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movies_count, len(response.data))

    def test_get_movies_by_title(self):
        title = 'Rocky'
        request = factory.get('/api/movies?title=' + title)
        response = movie_view(request)
        movies_count = Movie.objects.filter(title=title).count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movies_count, len(response.data))

    def test_get_movies_by_director(self):
        director = 'Renny Harlin'
        request = factory.get('/api/movies?director=' + director)
        response = movie_view(request)
        movies_count = Movie.objects.filter(director=director).count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movies_count, len(response.data))

    def test_movie_ordering(self):
        request = factory.get('/api/movies?ordering=year')
        response = movie_view(request)
        movies = Movie.objects.order_by('year')
        movies_count = movies.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movies_count, len(response.data))
        self.assertEqual(movies[0].imdb_id, response.data[0]['imdb_id'])
        self.assertEqual(movies[movies_count-1].imdb_id, response.data[movies_count-1]['imdb_id'])


class PostMovieTest(APITestCase):

    fixtures = ['fixtures.json']

    def test_post_movie_no_title(self):
        request = factory.post('/api/movies/')
        response = movie_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_movie_with_title(self):
        request = factory.post('/api/movies/', {'title': 'Citizen Kane'})
        response = movie_view(request)
        imdb_id = response.data['imdb_id']
        movie = Movie.objects.get(imdb_id=imdb_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(movie.title, response.data['title'])

    def test_post_existing_movie_with_title(self):
        request = factory.post('/api/movies/', {'title': 'Metropolis'})
        response = movie_view(request)
        imdb_id = response.data['imdb_id']
        movie = Movie.objects.get(imdb_id=imdb_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(movie.title, response.data['title'])



class GetCommentTest(APITestCase):

    fixtures = ['fixtures.json']

    def test_get_comments(self):
        request = factory.get('/api/comments/')
        response = comment_view(request)
        comment_count = Comment.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment_count, len(response.data))

    def test_get_comments_by_movie_id(self):
        movie_id = 4
        request = factory.get('/api/comments?movie_id=' + str(movie_id))
        response = comment_view(request)
        comment_count = Comment.objects.filter(movie_id=movie_id).count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment_count, len(response.data))

    def test_comment_ordering(self):
        request = factory.get('/api/comments?ordering=movie_id')
        response = comment_view(request)
        comments = Comment.objects.order_by('movie_id')
        comment_count = comments.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment_count, len(response.data))
        self.assertEqual(comments[0].movie.id, response.data[0]['movie'])
        self.assertEqual(comments[comment_count-1].movie.id, response.data[comment_count-1]['movie'])

class PostCommentTest(APITestCase):

    fixtures = ['fixtures.json']

    def test_post_comment_missing_comment_body(self):
        request = factory.post('/api/comments/', {'movie_id': 4})
        response = comment_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_comment_missing_movie_id(self):
        request = factory.post('/api/comments/', {'comment_body': 4})
        response = comment_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_comment(self):
        movie_id = 4
        comment_body = "Komentarz do filmu nr 4"
        comments_before_add_count = Comment.objects.filter(movie_id=movie_id).count()
        request = factory.post('/api/comments/', {'comment_body': comment_body, 'movie_id': movie_id})
        response = comment_view(request)
        comments = Comment.objects.filter(movie_id=movie_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(comment_body, [comment.body for comment in comments])
        self.assertEqual(comments_before_add_count + 1, comments.count())





