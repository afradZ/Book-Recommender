from django.urls import path
from . import views
from .views import rate_book, search_books
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('books/', views.fetch_books, name='fetch_books'),
    path('recommendations/', views.fetch_recommendations, name='fetch_recommendations'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('rate-book/', rate_book, name='rate_book'),
    path('search-books/', search_books, name='search_books'),
]