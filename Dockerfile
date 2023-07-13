# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the environment variables
ENV PORT=8080

# Expose the port that the application will listen on
EXPOSE $PORT

# Run the Flask application
CMD ["python", "app.py"]
