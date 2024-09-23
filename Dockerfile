FROM python:3.10.14-slim-bullseye

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update system and install dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    libgdal-dev build-essential libpq-dev apt-transport-https \
    ca-certificates gnupg curl gdal-bin libmariadb-dev-compat \
    libmariadb-dev libjpeg62-turbo-dev zlib1g-dev libwebp-dev \
    python-dev-is-python3 wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd --gid 1000 geouser && \
    useradd --uid 1000 --gid geouser --home /home/geouser --create-home geouser

# Set home directory and working directory
ENV HOME=/home/geouser
ENV APP_HOME=/home/geouser/agrowatcher
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Install Pipenv
RUN pip install pipenv

# Copy Pipfile and install dependencies
COPY ./Pipfile ./Pipfile.lock $APP_HOME/
RUN pipenv install --deploy --system --ignore-pipfile

# Install Google Cloud SDK
RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update -y && \
    apt-get install google-cloud-cli -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Service Account for authentication
COPY ee-bezalelbenuri-b751759fc97e.json /home/geouser/.config/gcloud/application_default_credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/home/geouser/.config/gcloud/application_default_credentials.json"

# Copy app code and set ownership
COPY . $APP_HOME
RUN chown -R geouser:geouser $APP_HOME

# Switch to the non-root user
USER geouser
