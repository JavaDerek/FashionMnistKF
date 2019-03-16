FROM tensorflow/tensorflow

COPY download.py .
RUN pip install minio
ENTRYPOINT ["python", "./download.py"]