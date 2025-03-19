from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

class Book(models.Model):
    google_books_id = models.TextField(unique=True)  # Unique ID from Google Books API
    title = models.CharField(max_length=200)
    authors = models.JSONField(default=list)  # Store multiple authors as a list
    description = models.TextField(blank=True, null=True)
    cover_image_url = models.URLField(blank=True, null=True)  # URL to the book cover
    published_date = models.CharField(max_length=10, blank=True, null=True)  # Year of publication

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Django's User model
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name= 'ratings')
    rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],  # Validate rating between 1-5
        default=3
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the rating was created

    class Meta:
        unique_together = ('user', 'book')  # Prevent duplicate ratings by the same user for the same book

    def __str__(self):
        return f"{self.user.username} rated {self.book.title} as {self.rating}"
