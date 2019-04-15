FROM python:2-stretch
ENV GEOSERVER_HOSTNAME http://geoseerver:8080
ENV GEOSERVER_USER admin
ENV GEOSERVER_PASSWORD geoserver
ADD ./data /opt/prepare_geoserver/
ADD ./prepare_geoserver.py /opt/prepare_geoserver/
RUN apt-get update && \
    apt-get install git -y && \
    apt-get install python-pip -y && \
    pip install gsconfig && \
    cd /opt/prepare_geoserver/
CMD  python prepare_geoserver.py ${GEOSERVER_HOSTNAME} ${GEOSERVER_USER} ${GEOSERVER_PASSWORD}
