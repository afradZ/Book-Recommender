# Use the official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY book_recommender_backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port for Railway
EXPOSE 8000

# Start the Gunicorn server
CMD ["gunicorn", "book_recommender_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
