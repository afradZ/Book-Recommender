console.log("script.js loaded successfully!");

const API_BASE_URL = 'http://127.0.0.1:8000/api/';

// Helper function to truncate the description
const truncateDescription = (text, maxLength) => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...'; // Add ellipsis for truncated text
};

// Fetch Books
const fetchBooks = async () => {
  try {
    const query = 'python';  // Default query to fetch books
    const url = `${API_BASE_URL}books/?q=${query}`;  // Add query parameter
    console.log('Fetching books from:', url);  // Debugging

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status} - ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Books data:', data);  // Debugging

    // Check if the response contains books data
    if (data.message === 'Books fetched and processed successfully') {
      // Fetch the saved books from your database
      const savedBooksResponse = await fetch(`${API_BASE_URL}search-books/?q=${query}`);
      if (!savedBooksResponse.ok) {
        throw new Error(`HTTP error! Status: ${savedBooksResponse.status} - ${savedBooksResponse.statusText}`);
      }

      const savedBooksData = await savedBooksResponse.json();
      console.log('Saved books data:', savedBooksData);  // Debugging
      displayBooks(savedBooksData, bookList);  // Display the saved books
    } else {
      console.error('Failed to fetch books:', data.error || 'Unknown error');
    }
  } catch (error) {
    console.error('Error fetching books:', error.message || error);
  }
};

// Rate Book
const rateBook = async (bookId, rating) => {
  console.log('Book ID:', bookId, 'Type:', typeof bookId);  // Debugging
  console.log('Rating value:', rating, 'Type:', typeof rating);  // Debugging
  const token = localStorage.getItem('token');
  if (!token) {
    alert('Please log in to rate books.');
    return;
  }

  // Convert rating to an integer
  const ratingInt = parseInt(rating, 10);

  // Validate rating
  if (isNaN(ratingInt) || ratingInt < 1 || ratingInt > 5) {
    alert('Rating must be an integer between 1 and 5.');
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}rate-book/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`,
      },
      body: JSON.stringify({ google_books_id: bookId, rating: ratingInt }),  // Use google_books_id
    });

    const data = await response.json();  // Parse the response as JSON

    if (response.ok) {
      alert('Rating saved successfully!');
      fetchBooks();  // Refresh the book list
    } else {
      console.error('Error response:', data);
      alert(`Failed to save rating: ${data.error || 'Unknown error'}`);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while saving the rating.');
  }
};

// Display Books
const displayBooks = (books, container) => {
  console.log('Displaying books:', books);  // Debugging
  console.log('Container:', container);  // Debugging

  if (container) {
    container.innerHTML = books
      .map(
        (book) => {
          // Calculate the average rating
          const avgRating = book.ratings?.length > 0
            ? (book.ratings.reduce((sum, rating) => sum + rating.rating, 0) / book.ratings.length)
            : null;

          return `
            <div class="book">
              <h3>${book.title}</h3>
              <p>Authors: ${book.authors?.join(', ') || 'No authors'}</p>
              <p class="description">
                <span class="truncated-description">${truncateDescription(book.description, 100)}</span>
                <span class="full-description" style="display: none;">${book.description}</span>
                <button class="read-more">Read More</button>
              </p>
              <div class="ratings">
                <strong>Average Rating:</strong>
                <p>${avgRating ? avgRating.toFixed(1) + ' stars' : 'No ratings yet'}</p>
              </div>
              <img src="${book.cover_image_url}" alt="${book.title}" width="100">
              <button class="rate-book" data-book-id="${book.google_books_id}">Rate this book</button>  <!-- Use google_books_id -->
            </div>
          `;
        }
      )
      .join('');

    // Add event listeners for "Read More" buttons
    const readMoreButtons = container.querySelectorAll('.read-more');
    readMoreButtons.forEach((button) => {
      button.addEventListener('click', (e) => {
        const description = e.target.closest('.description');
        const truncated = description.querySelector('.truncated-description');
        const full = description.querySelector('.full-description');

        if (full.style.display === 'none') {
          full.style.display = 'inline';
          truncated.style.display = 'none';
          e.target.textContent = 'Read Less';
        } else {
          full.style.display = 'none';
          truncated.style.display = 'inline';
          e.target.textContent = 'Read More';
        }
      });
    });

    // Add event listeners for "Rate this book" buttons
    const rateButtons = container.querySelectorAll('.rate-book');
    rateButtons.forEach((button) => {
      button.addEventListener('click', (e) => {
        const bookId = e.currentTarget.getAttribute('data-book-id');  // Use e.currentTarget
        console.log('Book ID:', bookId, 'Type:', typeof bookId);  // Debugging
        const rating = prompt('Rate this book (1-5 stars):');
        if (rating && rating >= 1 && rating <= 5) {
          rateBook(bookId, rating);  // Call the rateBook function
        } else {
          alert('Please enter a valid rating between 1 and 5.');
        }
      });
    });
  } else {
    console.error('Container not found');
  }
};

// Fetch Recommendations
const fetchRecommendations = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No token found. Please log in.');
      return;
    }

    const response = await fetch(`${API_BASE_URL}recommendations/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    displayBooks(data, recommendedBooks);
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const loginForm = document.getElementById('loginForm');
  const bookList = document.getElementById('books');
  const searchQuery = document.getElementById('searchQuery');
  const searchButton = document.getElementById('searchButton');
  const searchResults = document.getElementById('searchResults');
  const recommendedBooks = document.getElementById('recommendedBooks');
  const registerForm = document.getElementById('registerForm');

  // Login
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch(`${API_BASE_URL}login/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        localStorage.setItem('token', data.token);
        alert('Login successful!');
      } catch (error) {
        console.error('Error:', error);
        alert('Login failed. Please check your credentials.');
      }
    });
  } else {
    console.error('Login form not found');
  }

  // Register
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('regUsername').value;
      const email = document.getElementById('regEmail').value;
      const password = document.getElementById('regPassword').value;

      try {
        const response = await fetch(`${API_BASE_URL}register/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();
        if (response.ok) {
          alert('Registration successful! Please log in.');
        } else {
          alert('Registration failed. Please try again.');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    });
  }

  // Search Books
  if (searchButton && searchQuery) {
    searchButton.addEventListener('click', async () => {
      const query = searchQuery.value;
      if (!query) {
        alert('Please enter a search query.');
        return;
      }

      try {
        const url = `${API_BASE_URL}search-books/?q=${query}`;
        console.log('Searching books with query:', url);  // Debugging

        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        displayBooks(data, searchResults);  // Display search results
      } catch (error) {
        console.error('Error searching books:', error);
      }
    });
  } else {
    console.error('Search button or query input not found');
  }

  // Initial Load
  fetchBooks();
  fetchRecommendations();
});
