#/bin/bash

docker build . -t download
docker tag download dotnetderek/download:latest
docker push dotnetderek/download:latest