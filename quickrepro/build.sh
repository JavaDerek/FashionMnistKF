#/bin/bash

docker build . -t qr
docker tag qr dotnetderek/qr:latest
docker push dotnetderek/qr:latest