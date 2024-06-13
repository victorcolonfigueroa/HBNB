# Start with an appropriate Alpine Linux base image with Python
FROM python:3.8-alpine

# Set a directory for the app
WORKDIR /usr/src/app

# Copy the application source code into the container
COPY . .

# Utilize a requirements.txt to manage Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script into the Docker image
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Set the script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Define an environment variable for the port in your Dockerfile
ENV PORT 8000

# Expose the port
EXPOSE 8000

# Define a volume in your Dockerfile where your application will store its persistent data
VOLUME /usr/src/app/data
