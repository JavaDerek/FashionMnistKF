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
numpy.save('/train_labels', train_labels)
numpy.save('/test_images', test_images)
numpy.save('/test_labels', test_labels)

try:
    with open('/train_images.npy', 'rb') as file_data:
        file_stat = os.stat('/train_images.npy')
        print(minioClient.put_object('fashionmnist', 'trainimages',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

text_file = open("trainImagesObjectName.txt", "w")
text_file.write('trainimages')
text_file.close()

try:
    with open('/train_labels.npy', 'rb') as file_data:
        file_stat = os.stat('/train_labels.npy')
        print(minioClient.put_object('fashionmnist', 'trainlabels',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

text_file = open("trainLabelsObjectName.txt", "w")
text_file.write('trainlabels')
text_file.close()

try:
    with open('/test_images.npy', 'rb') as file_data:
        file_stat = os.stat('/test_images.npy')
        print(minioClient.put_object('fashionmnist', 'testimages',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

text_file = open("testImagesObjectName.txt", "w")
text_file.write('testimages')
text_file.close()

try:
    with open('/test_labels.npy', 'rb') as file_data:
        file_stat = os.stat('/test_labels.npy')
        print(minioClient.put_object('fashionmnist', 'testlabels',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

text_file = open("testLabelsObjectName.txt", "w")
text_file.write('testlabels')
text_file.close()