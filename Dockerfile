# Set the base image to use to Ubuntu
FROM ubuntu:16.10

# Set the file maintainer
MAINTAINER Richard Tong

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
# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ
COPY requirements.txt $DOCKYARD_SRVPROJ
# Install Python dependencies
RUN pip install -r $DOCKYARD_SRVPROJ/requirements.txt
# Port to expose
EXPOSE 8000
# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./gunicorn-start.sh /
# intend gunicorn-start to be the entrypoint command for this image
ENTRYPOINT ["/gunicorn-start.sh"]