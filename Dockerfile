# Use an appropriate base image
FROM python:3.8-alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy the application source code to the container
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for the file storage and set permissions
RUN mkdir -p /usr/src/app/storage && \
    chmod -R 777 /usr/src/app/storage

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run"]
