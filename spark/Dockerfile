FROM bitnami/spark:latest
LABEL authors="viane"

USER root

# Copy the local package files to the container's workspace.
COPY . /app

# Set the working directory
WORKDIR /app

# Install the packages from the requirements file.
RUN pip3 install -r requirements.txt

# Run the application.
ENTRYPOINT ["/bin/bash", "/app/start-spark.sh"]