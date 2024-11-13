# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./app/requirements.txt /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code into the container
COPY ./app /app

# Expose the port on which the app will run
EXPOSE 8050

# Set environment variables to handle specific Dash configurations
ENV DASH_DEBUG_MODE=True

# Command to run the app
CMD ["python", "app.py"]
