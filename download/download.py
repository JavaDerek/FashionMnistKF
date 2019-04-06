from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy
from tensorflow import keras
import numpy as np
from minio import Minio
from minio.error import ResponseError
import os
import sys
import pickle

print(tf.__version__)

if (sys.argv[1] == "full"):
    minioClient = Minio('172.17.0.39:9000',
        access_key='AKIAIOSFODNN7EXAMPLE',
        secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        secure=False)

    print('Instantiated Minio client')

    if minioClient.bucket_exists("fashionmnist"):
        objects = minioClient.list_objects('fashionmnist', recursive=True)
        for obj in objects:
            minioClient.remove_object('fashionmnist',obj.object_name.encode('utf-8'))

        print('Emptied existing fashionmnist bucket')
        minioClient.remove_bucket("fashionmnist")
        print('Removed existing fashionmnist bucket')

    minioClient.make_bucket("fashionmnist")
    print('Created new fashionmnist bucket')

    fashion_mnist = keras.datasets.fashion_mnist

    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    pickle.dump( train_images, open( "/train_images", "wb" ), pickle.HIGHEST_PROTOCOL )
    pickle.dump( train_labels, open( "/train_labels", "wb" ), pickle.HIGHEST_PROTOCOL )
    pickle.dump( test_images, open( "/test_images", "wb" ), pickle.HIGHEST_PROTOCOL )
    pickle.dump( test_labels, open( "/test_labels", "wb" ), pickle.HIGHEST_PROTOCOL )

    try:
        with open('/train_images', 'rb') as file_data:
            file_stat = os.stat('/train_images')
            print(minioClient.put_object('fashionmnist', 'trainimages',
                                file_data, file_stat.st_size))
    except ResponseError as err:
        print(err)

    try:
        with open('/train_labels', 'rb') as file_data:
            file_stat = os.stat('/train_labels')
            print(minioClient.put_object('fashionmnist', 'trainlabels',
                                file_data, file_stat.st_size))
    except ResponseError as err:
        print(err)

    try:
        with open('/test_images', 'rb') as file_data:
            file_stat = os.stat('/test_images')
            print(minioClient.put_object('fashionmnist', 'testimages',
                                file_data, file_stat.st_size))
    except ResponseError as err:
        print(err)

    try:
        with open('/test_labels', 'rb') as file_data:
            file_stat = os.stat('/test_labels')
            print(minioClient.put_object('fashionmnist', 'testlabels',
                                file_data, file_stat.st_size))
    except ResponseError as err:
        print(err)

text_file = open("trainImagesObjectName.txt", "w")
text_file.write('trainimages')
text_file.close()

text_file = open("trainLabelsObjectName.txt", "w")
text_file.write('trainlabels')
text_file.close()

text_file = open("testImagesObjectName.txt", "w")
text_file.write('testimages')
text_file.close()

text_file = open("testLabelsObjectName.txt", "w")
text_file.write('testlabels')
text_file.close()