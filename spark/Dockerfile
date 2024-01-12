FROM bitnami/spark:latest
LABEL authors="viane"


# Define a build-time argument
ARG SPARK_HOME=/opt/bitnami/spark
ARG APP_FOLDER=${SPARK_HOME}/app

ADD ./postgresql-42.7.1.jar ${SPARK_HOME}/jars/

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

