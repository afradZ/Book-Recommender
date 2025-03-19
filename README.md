 Book Recommender

This is my submission for: ALX Build Your Portfolio Project, is a Django & JavaScript-powered book recommendation system that allows users to search for books, get recommendations, and rate books.

🌟 Features

🔑 Authentication System
Users can register and log in.
Authentication is handled using Token Authentication in Django REST Framework.
📖 Book Search
Users can search for books by title, author, or description.
The search fetches results from the Google Books API.

🌟 Book Recommendations
Users receive personalized book recommendations based on:
Top-rated books in the database.
Future: User preferences & ratings.

⭐ Book Rating
Logged-in users can rate books (1-5 stars).
Users can update their rating for a book.
🔗 API Endpoints
Method	Endpoint	Description
POST	/api/register/	Register a new user
POST	/api/login/	User login (returns a token)
GET	/api/fetch-books/	Get all books in the database
GET	/api/search-books/	Search books using Google Books API
GET	/api/recommendations/	Get book recommendations
POST	/api/rate-book/	Rate a book (1-5 stars)

🚀 How to Use
1️⃣ Register & Log in
2️⃣ Search for books or get recommendations
3️⃣ Rate books and update your ratings
4️⃣ Enjoy reading! 📖✨

🛠️ Technologies Used
Backend: Django, Django REST Framework
Database: PostgreSQL
Frontend: HTML, CSS, JavaScript
External API: Google Books API

📝 Future Improvements
✅ Better recommendation system (AI-based suggestions)
✅ User profiles & reading lists
✅ Improved UI/UX with animations

📌 Contributions are welcome! Fork the repo and submit a pull request. 🚀🎉
