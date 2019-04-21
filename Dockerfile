FROM python:2-stretch
#ENV GEOSERVER_HOSTNAME http://geoseerver:8080
#ENV GEOSERVER_USER admin
#ENV GEOSERVER_PASSWORD geoserver
ADD ./data /opt/prepare_geoserver/
ADD ./prepare_geoserver.py /opt/prepare_geoserver/
ADD ./wait_geoserver.sh /opt/prepare_geoserver/
ADD ./data /var/prepare_geoserver/data
RUN apt-get update && \
    apt-get install git -y && \
    apt-get install python-pip -y && \
    pip install gsconfig 
