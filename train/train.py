from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy
from tensorflow import keras
import numpy as np
from minio import Minio
from minio.error import ResponseError
import os
import sys
import tempfile
import tarfile
import pickle

print(tf.__version__)

model = keras.Sequential([
  keras.layers.Conv2D(input_shape=(28,28,1), filters=8, kernel_size=3, 
                      strides=2, activation='relu', name='Conv1'),
  keras.layers.Flatten(),
  keras.layers.Dense(10, activation=tf.nn.softmax, name='Softmax')
])
model.summary()

print('Created an untrained keras model')

testing = False
epochs = 5

model.compile(optimizer=tf.train.AdamOptimizer(), 
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
    with open('trainimages', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Training images retrieved from S3 to local file system')

train_images = pickle.load( open( "trainimages", "rb" ) )

print('Training images retrieved from local file system to Numpy array')

#---

print(bucketNameForTrainLabels)

try:
    data = minioClient.get_object('fashionmnist', bucketNameForTrainLabels)
    with open('trainlabels', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Training labels retrieved from S3 to local file system')

train_labels = pickle.load( open( "trainlabels", "rb" ) )

print('Training labels retrieved from local file system to Numpy array')

#---

print('\ntrain_images.shape: {}, of {}'.format(train_images.shape, train_images.dtype))

model.fit(train_images, train_labels, epochs=epochs)

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