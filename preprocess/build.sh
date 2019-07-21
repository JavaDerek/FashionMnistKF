#/bin/bash

docker build . -t preprocess
docker tag preprocess dotnetderek/preprocess:vop
docker push dotnetderek/preprocess:vop