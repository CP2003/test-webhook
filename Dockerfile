# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy your application files to the container
COPY main.py /app/
COPY bot /app/bot/

# Install any required dependencies
# For example, if you have a requirements.txt file, you can use it like this:
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Define the command to run your application
CMD ["python", "Nawodya/__main__.py"]
