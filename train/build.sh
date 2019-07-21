#/bin/bash

docker build . -t train
docker tag train dotnetderek/train:vop
docker push dotnetderek/train:vop