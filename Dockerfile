# Set the base image to use to Ubuntu
FROM ubuntu:16.10

# Set the file maintainer
MAINTAINER Richard Tong

# Export DJANGO_SETTINGS_MODULE here
ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE}

# Set env path variables used in this Dockerfile
ENV DOCKYARD_SRC=src
ENV DOCKYARD_SRVHOME=/srv
ENV DOCKYARD_SRVPROJ=$DOCKYARD_SRVHOME/$DOCKYARD_SRC

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3.6 python-pip python3.6-dev nginx

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs
VOLUME ["$DOCKYARD_SRVHOME/media/", "$DOCKYARD_SRVHOME/logs/"]

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./gunicorn-start.sh /

# Copy server block for nginx
COPY ./django_nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# intend gunicorn-start to be the entrypoint command for this image
CMD ["/gunicorn-start.sh"]