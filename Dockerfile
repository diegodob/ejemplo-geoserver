FROM python:2-stretch
#ENV GEOSERVER_HOSTNAME http://geoseerver:8080
#ENV GEOSERVER_USER admin
#ENV GEOSERVER_PASSWORD geoserver
#TODO DOB 23-04-19: Definir el repositorio GIT en una variable de entorno
ADD ./goblocal-inicio.py /opt/goblocal-inicio/
ADD ./wait-goblocal-geoserver.sh /opt/goblocal-inicio/
RUN apt-get update && \
    apt-get install git -y && \
    apt-get install python-pip -y && \
    pip install gsconfig  
