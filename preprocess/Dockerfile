FROM publysher/alpine-numpy

COPY preprocess.py .
RUN pip install minio
ENTRYPOINT ["python", "./preprocess.py"]