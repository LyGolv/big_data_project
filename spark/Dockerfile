FROM bitnami/spark:latest
LABEL authors="viane"

USER root

# Define a build-time argument
ARG APP_FOLDER=/opt/bitnami/spark/app

# Copy the local package files to the container's workspace.
COPY . ${APP_FOLDER}

# Set the working directory
WORKDIR ${APP_FOLDER}

# Install the packages from the requirements file.
RUN pip3 install -r requirements.txt

# Run the application.
ENTRYPOINT ["/bin/bash", "/opt/bitnami/spark/app/spark-config.sh"]
# ecrase la commande de l'image de base
CMD [ "" ]