from __future__ import absolute_import, division, print_function

import numpy
from tensorflow import keras
import tensorflow as tf
import sys
import os
import requests

print('Evaluate started')

model = keras.models.load_model('/mnt/my_model.h5')

model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print('Model retrieved from local file system to Keras model')

#---

test_images = numpy.load('/mnt/test_images')

print('Test images retrieved from local file system to Keras model')

#---

test_labels = numpy.load('/mnt/test_labels')

print('Test labels retrieved from local file system to Keras model')

#---

test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)

#Have to figure out what to do about *actually* serving this!
#r = requests.get('http://10.10.10.10:5000')
#print(r.text)