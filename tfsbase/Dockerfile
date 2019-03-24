FROM tensorflow/serving

RUN apt-get update
RUN apt-get -y install python python-pip
RUN pip install -U Flask
RUN pip install numpy
RUN pip install minio

COPY runner.sh /
COPY it.py /it.py

RUN chmod +x /runner.sh

ENTRYPOINT ["bash", "/runner.sh"]