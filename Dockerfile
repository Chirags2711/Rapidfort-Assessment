# Use Python 3.12 slim as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (or any other available port)
EXPOSE 8000

# Set the environment variable to use Python 3.12
ENV FLASK_ENV=development

# Run the application, making it listen on all available network interfaces
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]