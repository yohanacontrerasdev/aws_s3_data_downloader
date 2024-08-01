# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /usr/src/app

# Add current directory files to the container at /usr/src/app
ADD . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]