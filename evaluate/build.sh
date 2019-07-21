#/bin/bash

docker build . -t evaluate
docker tag evaluate dotnetderek/evaluate:vop
docker push dotnetderek/evaluate:vop