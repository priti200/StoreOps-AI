# Use an official lightweight Python image.
FROM python:3.10-slim

# Set the working directory inside the container.
WORKDIR /code

# Copy requirements FIRST to leverage Docker cache.
COPY app/requirements.txt /code/requirements.txt

# Install dependencies.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code.
COPY app /code/app
COPY .env /code/.env

# Create the data directory if it doesn't exist (for safety).
RUN mkdir -p /code/app/data

# Expose the port the app runs on.
EXPOSE 8000

# Command to run the application using Uvicorn.
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
