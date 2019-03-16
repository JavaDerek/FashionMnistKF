#/bin/bash

docker build . -t download
docker tag download dotnetderek/download:031619
docker push dotnetderek/download:031619