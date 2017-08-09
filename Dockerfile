# Set the base image to use to Ubuntu
FROM ubuntu:16.10

# Set the file maintainer
MAINTAINER Richard Tong

# Take a build arg specifying an argument to gunicorn-start.sh
# Specify which DJANGO_PROJECT_SETTINGS {'staging', 'production'} to use
# Export DJANGO_SETTINGS_MODULE here
ARG DJANGO_PROJECT_SETTINGS
ENV DJANGO_SETTINGS_MODULE ${DJANGO_PROJECT_SETTINGS}

# Set env variables used in this Dockerfile
# Local directory with project source
ENV DOCKYARD_SRC=src

# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv

# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=$DOCKYARD_SRVHOME/$DOCKYARD_SRC

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3.6 python-pip python3.6-dev

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./gunicorn-start.sh /

# intend gunicorn-start to be the entrypoint command for this image
ENTRYPOINT ["/gunicorn-start.sh"]