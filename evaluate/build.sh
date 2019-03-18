#/bin/bash

docker build . -t evaluate
docker tag evaluate dotnetderek/evaluate:latest
docker push dotnetderek/evaluate:latest