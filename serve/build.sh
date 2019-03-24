#/bin/bash

docker build . -t serve
docker tag serve dotnetderek/serve:latest
docker push dotnetderek/serve:latest