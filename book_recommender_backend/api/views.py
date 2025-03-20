import logging
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings
import requests
from .models import Book, Rating
from .serializers import BookSerializer, RatingSerializer, UserSerializer
from django.db.models import Q, Avg

# Set up logging
logger = logging.getLogger(__name__)

# Google Books API settings
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# Fetch books from Google Books API
@api_view(['GET'])
def fetch_books(request):
    query = request.query_params.get('q', '')  # Default to empty string if no query
    params = {
        'q': query,
        'maxResults': 10,
        'key': settings.GOOGLE_BOOKS_API_KEY
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code == 200:
        books_data = response.json().get('items', [])
        for book in books_data:
            volume_info = book.get('volumeInfo', {})
            google_books_id = book.get('id')
            title = volume_info.get('title', 'No Title')
            authors = volume_info.get('authors', [])
            description = volume_info.get('description', 'No Description')
            cover_image_url = volume_info.get('imageLinks', {}).get('thumbnail', '')
            published_date = volume_info.get('publishedDate', '')

            # Check if the book already exists in the database
            if not Book.objects.filter(google_books_id=google_books_id).exists():
                # Create a new Book instance
                Book.objects.create(
                    google_books_id=google_books_id,
                    title=title,
                    authors=authors,
                    description=description,
                    cover_image_url=cover_image_url,
                    published_date=published_date,
                )

        # Fetch only the books that match the query from the database
        matching_books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query) |
            Q(description__icontains=query)
        ).prefetch_related('ratings')  # Use the correct related_name
        serializer = BookSerializer(matching_books, many=True)
        return Response(serializer.data)
    return Response({'error': 'Failed to fetch books'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#rate a book
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rate_book(request):
    try:
        google_books_id = request.data.get('google_books_id')  # Use google_books_id
        rating_value = request.data.get('rating')

        # Validate google_books_id and rating_value
        if not google_books_id or not rating_value:
            return Response({'error': 'google_books_id and rating are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert rating_value to an integer
        try:
            rating_value = int(rating_value)
        except (ValueError, TypeError):
            return Response({'error': 'Rating must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate rating_value
        if rating_value < 1 or rating_value > 5:
            return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the book or return 404 if not found
        try:
            book = Book.objects.get(google_books_id=google_books_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already rated this book
        rating, created = Rating.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'rating': rating_value}
        )

        if not created:
            rating.rating = rating_value
            rating.save()

        return Response({'message': 'Rating saved successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Log the error for debugging
        print(f"Error in rate_book view: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Fetch personalized recommendations
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_recommendations(request):
    # Annotate each book with its average rating, excluding books with no ratings
    top_books = Book.objects.annotate(
        avg_rating=Avg('ratings__rating')
    ).filter(
        ratings__isnull=False  # Exclude books with no ratings
    ).order_by(
        '-avg_rating'  # Order by average rating in descending order
    )[:10]  # Limit to top 10 books

    if not top_books:
        return Response({'error': 'No recommendations found'}, status=200)
    
    serializer = BookSerializer(top_books, many=True)
    return Response(serializer.data, status=200)

#search books   
@api_view(['GET'])
def search_books(request):
    query = request.query_params.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(authors__icontains=query) |
        Q(description__icontains=query)
    )
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
  
#User registration
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
           username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=request.data.get('password')
        )
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User login (returns auth token)
@api_view(['POST'])
def login_user(request):
    from rest_framework.authtoken.models import Token
    user = User.objects.get(username=request.data['username'])
    if user.check_password(request.data['password']):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
