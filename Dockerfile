# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]