FROM ubuntu:latest
LABEL authors="lygolv"

# Install the necessary packages
RUN apt-get update && \
    apt-get install -y python3-pip

# Copy the local package files to the container's workspace.
ADD . /app

# Set the working directory
WORKDIR /app

# Install the packages from the requirements file.
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the application.
ENTRYPOINT ["python3", "main.py"]