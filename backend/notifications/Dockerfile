# Use Python 3.9 image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app.py /app/

# Expose port 5001 for Notification Service
EXPOSE 5001

# Command to run the Flask app
CMD ["python", "app.py"]

