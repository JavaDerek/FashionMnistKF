FROM tensorflow/serving:latest-devel

RUN pip install numpy
RUN pip install minio

COPY blowup.py .
ENTRYPOINT ["python", "blowup.py"]