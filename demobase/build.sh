#/bin/bash

docker build . -t demobase
docker tag demobase dotnetderek/demobase:latest
docker push dotnetderek/demobase:latest