#/bin/bash

docker build . -t download
docker tag download dotnetderek/download:vop
docker push dotnetderek/download:vop