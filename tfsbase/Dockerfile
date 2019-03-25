FROM tensorflow/serving:latest-devel

RUN apt-get update
#RUN apt-get -y install python python-pip
RUN pip install -U Flask
RUN pip install numpy
RUN pip install minio
#RUN pip install tensorflow==2.0.0-alpha0

COPY runner.sh /
COPY it.py /it.py

RUN chmod +x /runner.sh

ENTRYPOINT ["bash", "/runner.sh"]