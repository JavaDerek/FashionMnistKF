from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy
from tensorflow import keras
import numpy as np
import os
import sys
import tempfile
import tarfile
import pickle
from time import time
from tensorflow.python.keras.callbacks import TensorBoard

print(tf.__version__)

tensorboard = TensorBoard(log_dir="/logdir")

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

train_images = pickle.load( open( "/mnt/train_images", "rb" ) )

print('Training images retrieved from local file system to Numpy array')

#---

train_labels = pickle.load( open( "/mnt/train_labels", "rb" ) )

print('Training labels retrieved from local file system to Numpy array')

#---

print('\ntrain_images.shape: {}, of {}'.format(train_images.shape, train_images.dtype))

model.fit(train_images, train_labels, epochs=epochs, callbacks=[tensorboard])

print('Training finished')

model.save('/mnt/my_model.h5')
print("Saved model to local disk")

#---

# This won't work with KF's viewer yet
# md_file = open("/mnt/mlpipeline-ui-metadata.json", "w")
# md_file.write('{"version": 1,"outputs": [{"type": "tensorboard","source": "/logdir"}]}')
# md_file.close()

# print('Wrote tensorboard metadata')

print("starting to write conclusion message")
text_file = open("trainOk.txt", "w+")
text_file.write('ok')
text_file.close()
print("wrote conclusion message")