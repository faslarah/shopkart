# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Prevent Python from writing .pyc files to disk and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project code into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# The command that starts the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
