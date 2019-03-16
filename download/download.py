from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy
from tensorflow import keras
import numpy as np
from minio import Minio
from minio.error import ResponseError
import os

print(tf.__version__)

minioClient = Minio('172.17.0.39:9000',
    access_key='AKIAIOSFODNN7EXAMPLE',
    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    secure=False)

print('Instantiated Minio client')

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

try:
    if not(minioClient.bucket_exists("fashionmnist")):
        print("Made fashionmnist bucket")
        minioClient.make_bucket("fashionmnist")
    else:
        print("fashionmnist exists")
except ResponseError as err:
    print(err)

numpy.save('/train_images', train_images)

# Put a file with default content-type, upon success prints the etag identifier computed by server.
try:
    with open('/train_images.npy', 'rb') as file_data:
        file_stat = os.stat('/train_images.npy')
        print(minioClient.put_object('fashionmnist', 'trainimages',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

#numpy.save('train_labels', train_labels)
#numpy.save('test_images', test_images)
#numpy.save('test_labels', test_labels)