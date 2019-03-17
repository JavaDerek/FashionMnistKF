#/bin/bash

docker build . -t preprocess
docker tag preprocess dotnetderek/preprocess:latest
docker push dotnetderek/preprocess:latest