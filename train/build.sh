#/bin/bash

docker build . -t train
docker tag train dotnetderek/train:latest
docker push dotnetderek/train:latest