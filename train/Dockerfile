FROM tensorflow/serving:latest-devel

COPY train.py .
RUN pip install minio

ENTRYPOINT ["python", "./train.py"]