FROM tensorflow/tensorflow

COPY train.py .
RUN pip install minio

ENTRYPOINT ["python", "./train.py"]