from __future__ import absolute_import, division, print_function

import numpy
from minio import Minio
from minio.error import ResponseError
from tensorflow import keras
import tensorflow as tf
import sys
import os
import requests

print('Evaluate started')

minioClient = Minio('172.17.0.44:9000',
    access_key='AKIAIOSFODNN7EXAMPLE',
    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    secure=False)

print('Instantiated Minio client')

if len(sys.argv) > 2:
    bucketNameForTestImages = sys.argv[1]
    bucketNameForTestLabels = sys.argv[2]
    bucketNameForModel = sys.argv[3]
else:
    bucketNameForTestImages = 'normalizedtestimages'
    bucketNameForTestLabels = 'testlabels'
    bucketNameForModel = 'trainedmodel'

print(bucketNameForModel)
print(bucketNameForTestImages)
print(bucketNameForTestLabels)

try:
    data = minioClient.get_object('fashionmnist', bucketNameForModel)
    with open('model.h5', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Model retrieved from S3 to local file system')

model = keras.models.load_model('model.h5')

model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print('Model retrieved from local file system to Keras model')

#---

try:
    data = minioClient.get_object('fashionmnist', bucketNameForTestImages)
    with open('testimages.npy', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Test images retrieved from S3 to local file system')

test_images = numpy.load('testimages.npy')

print('Test images retrieved from local file system to Keras model')

#---

try:
    data = minioClient.get_object('fashionmnist', bucketNameForTestLabels)
    with open('testlabels.npy', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Test labels retrieved from S3 to local file system')

test_labels = numpy.load('testlabels.npy')

print('Test labels retrieved from local file system to Keras model')

#---

test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)

r = requests.get('http://10.10.10.10:5000')
print(r.text)