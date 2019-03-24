#/bin/bash

FLASK_APP=/it.py flask run --host=0.0.0.0 &
/usr/bin/tf_serving_entrypoint.sh