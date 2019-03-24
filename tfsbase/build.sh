#/bin/bash

docker build . -t tfsbase
docker tag tfsbase dotnetderek/tfsbase:latest
docker push dotnetderek/tfsbase:latest