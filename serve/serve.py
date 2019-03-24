from __future__ import absolute_import, division, print_function

import numpy
from minio import Minio
from minio.error import ResponseError
import sys
import os

print('serve started')

minioClient = Minio('172.17.0.39:9000',
    access_key='AKIAIOSFODNN7EXAMPLE',
    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    secure=False)

print('Instantiated Minio client')

if len(sys.argv) > 2:
    bucketNameForModel = sys.argv[3]
else:
    bucketNameForModel = 'trainedmodel'

print(bucketNameForModel)

try:
    data = minioClient.get_object('fashionmnist', bucketNameForModel)
    with open('model.h5', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Model retrieved from S3 to local file system')