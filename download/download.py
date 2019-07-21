from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy
from tensorflow import keras
import numpy as np
import os
import sys
import pickle

print(tf.__version__)

if (sys.argv[1] == "full"):

    fashion_mnist = keras.datasets.fashion_mnist

    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    print("starting to dump download to files")

    pickle.dump( train_images, open( "/mnt/train_images", "wb" ), pickle.HIGHEST_PROTOCOL )
    pickle.dump( train_labels, open( "/mnt/train_labels", "wb" ), pickle.HIGHEST_PROTOCOL )
    pickle.dump( test_images, open( "/mnt/test_images", "wb" ), pickle.HIGHEST_PROTOCOL )
    pickle.dump( test_labels, open( "/mnt/test_labels", "wb" ), pickle.HIGHEST_PROTOCOL )

    print("starting to write conclusion message")
    text_file = open("downloadOk.txt", "w")
    text_file.write('ok')
    text_file.close()