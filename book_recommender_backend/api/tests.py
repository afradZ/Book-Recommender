from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Rating
from rest_framework.authtoken.models import Token

class BookTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create a test book
        self.book = Book.objects.create(
            google_books_id='test-id',
            title='Test Book',
            authors=['Test Author'],
            description='Test Description',
            cover_image_url='http://example.com/cover.jpg',
            published_date='2023-01-01'
        )

    # Test fetching books from Google Books API
    def test_fetch_books(self):
        url = reverse('fetch-books')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    # Test rating a book
    def test_rate_book(self):
        url = reverse('rate-book')
        data = {
            'google_books_id': self.book.google_books_id,
            'rating': 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Rating saved successfully')

    # Test fetching personalized recommendations
    def test_fetch_recommendations(self):
        url = reverse('fetch-recommendations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test searching books
    def test_search_books(self):
        url = reverse('search-books')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    # Test user registration
    def test_register_user(self):
        url = reverse('register-user')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')

    # Test user login
    def test_login_user(self):
        url = reverse('login-user')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    # Test invalid login
    def test_invalid_login(self):
        url = reverse('login-user')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid credentials')
