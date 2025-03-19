from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Book, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'rating', 'created_at']

class BookSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)  # Include all ratings
    avg_rating = serializers.SerializerMethodField()  # Add average rating field

    class Meta:
        model = Book
        fields = ['google_books_id', 'title', 'authors', 'description', 'cover_image_url', 'ratings', 'avg_rating']

    def get_avg_rating(self, obj):
        # Calculate the average rating for the book
        return obj.ratings.aggregate(Avg('rating'))['rating__avg']