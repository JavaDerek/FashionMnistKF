FROM tensorflow/tensorflow

COPY preprocess.py .
RUN pip install minio
ENTRYPOINT ["python", "./preprocess.py"]