FROM python:3.9-slim-buster
LABEL authors="lygolv"

ARG APP_PATH=/dashboard

# Copy the local package files to the container's workspace.
RUN mkdir ${APP_PATH}

# Set the working directory
WORKDIR ${APP_PATH}

COPY main.py ${APP_PATH}/main.py
COPY requirements.txt ${APP_PATH}/requirements.txt

# Install the packages from the requirements file.
RUN pip3 install -r requirements.txt

EXPOSE 5432

# Run the application.
ENTRYPOINT ["python3", "main.py"]