from __future__ import absolute_import, division, print_function
from flask import Flask
import numpy
from minio import Minio
from minio.error import ResponseError
import sys
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    minioClient = Minio('172.17.0.39:9000',
        access_key='AKIAIOSFODNN7EXAMPLE',
        secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        secure=False)
    print('Instantiated Minio client')
    bucketNameForModel = 'trainedmodel'

    try:
        data = minioClient.get_object('fashionmnist', bucketNameForModel)
        with open('model.h5', 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)
    except ResponseError as err:
        print(err)

    print('Model retrieved from S3 to local file system')

    return 'Got data'


if __name__ == '__main__':
    print('tfsbase started')
    app.run(debug=True, host='0.0.0.0')
