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

bucketNameForTestImages = 'normalizedtestimages'
bucketNameForTestLabels = 'testlabels'

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

#---

try:
    data = minioClient.get_object('fashionmnist', bucketNameForTestImages)
    with open('testimages', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Test images retrieved from S3 to local file system')

test_images = pickle.load( open( "testimages", "rb" ) )

print('Test images retrieved from local file system to Keras model')

#---

try:
    data = minioClient.get_object('fashionmnist', bucketNameForTestLabels)
    with open('testlabels', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Test labels retrieved from S3 to local file system')

test_labels = pickle.load( open( "testlabels", "rb" ) )

print('Test labels retrieved from local file system to Keras model')

#---

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
print('test_images.shape: {}, of {}'.format(test_images.shape, test_images.dtype))

model.fit(train_images, train_labels, epochs=epochs)

print('Training finished')

test_loss, test_acc = model.evaluate(test_images, test_labels)
print('\nTest accuracy: {}'.format(test_acc))

MODEL_DIR = tempfile.gettempdir()
version = 1
export_path = os.path.join(MODEL_DIR, str(version))
print('export_path = {}\n'.format(export_path))

tf.saved_model.simple_save(
    keras.backend.get_session(),
    export_path,
    inputs={'input_image': model.input},
    outputs={t.name:t for t in model.outputs})

print("Saved model to local disk")

tar = tarfile.open("TarName.tar.gz", "w:gz")
tar.add(export_path, arcname="TarName")
tar.close()

print("Tarred up the directory")
#
#---

try:
    with open('TarName.tar.gz', 'rb') as file_data:
        file_stat = os.stat('TarName.tar.gz')
        print(minioClient.put_object('fashionmnist', 'trainedmodel',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

text_file = open("trainedModelName.txt", "w")
text_file.write('trainedmodel')
text_file.close()

print('Stored trained model in S3')