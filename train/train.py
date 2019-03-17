from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy
from tensorflow import keras
import numpy as np
from minio import Minio
from minio.error import ResponseError
import os
import sys

print(tf.__version__)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

print('Created an untrained keras model')

model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print('Compiled the model')

minioClient = Minio('172.17.0.39:9000',
    access_key='AKIAIOSFODNN7EXAMPLE',
    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    secure=False)

print('Instantiated Minio client')

if len(sys.argv) > 2:
    bucketNameForTrainImages =  sys.argv[1]
    bucketNameForTrainLabels = sys.argv[2]
else:
    bucketNameForTrainImages =  'normalizedtrainimages'
    bucketNameForTrainLabels = 'trainlabels'

print(bucketNameForTrainImages)
print(bucketNameForTrainLabels)

try:
    data = minioClient.get_object('fashionmnist', bucketNameForTrainImages)
    with open('train_images', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Training images retrieved from S3 to local file system')

train_images = numpy.load('train_images')

print('Training images retrieved from local file system to Numpy array')

#---

print(bucketNameForTrainLabels)

try:
    data = minioClient.get_object('fashionmnist', bucketNameForTrainLabels)
    with open('train_labels', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Training labels retrieved from S3 to local file system')

train_labels = numpy.load('train_labels')

print('Training labels retrieved from local file system to Numpy array')

#---

model.fit(train_images, train_labels, epochs=5)

print('Training finished')

model.save('my_model.h5')
print("Saved model to local disk")

#---

try:
    with open('my_model.h5', 'rb') as file_data:
        file_stat = os.stat('my_model.h5')
        print(minioClient.put_object('fashionmnist', 'trainedmodel',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

text_file = open("trainedModelName.txt", "w")
text_file.write('trainedmodel')
text_file.close()

print('Stored trained model in S3')