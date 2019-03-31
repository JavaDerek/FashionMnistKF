FROM tensorflow/serving:latest-devel

COPY evaluate.py .
RUN pip install minio

ENTRYPOINT ["python", "./evaluate.py"]