#/bin/bash

FLASK_APP=/it.py flask run --host=0.0.0.0 &
tensorflow_model_server --rest_api_port=8501 --port=8500 --model_name=mnist --model_base_path=/tmp/mnist_model/