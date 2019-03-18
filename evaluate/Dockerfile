FROM tensorflow/tensorflow

COPY evaluate.py .
RUN pip install minio
ENTRYPOINT ["python", "./evaluate.py"]