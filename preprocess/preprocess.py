from __future__ import absolute_import, division, print_function

import numpy
import sys
import os
import json
import pickle

print('Preprocess started')

if (sys.argv[1] == "full"):

    train_images = pickle.load( open( "/mnt/train_images", "rb" ) )

    print('Training images retrieved from local file system to Numpy array')

    #---

    train_labels = pickle.load( open( "/mnt/train_labels", "rb" ) )

    print('Training labels retrieved from local file system to Numpy array')

    #---

    test_images = pickle.load( open( "/mnt/test_images", "rb" ) )

    print('Test images retrieved from local file system to Numpy array')

    #---

    test_labels = pickle.load( open( "/mnt/test_labels", "rb" ) )

    print('Test labels retrieved from local file system to Numpy array')

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    # reshape for feeding into the model - DMF March 30, 2019 - Please let this work! :-)
    train_images = train_images.reshape(train_images.shape[0], 28, 28, 1)
    test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)

    print('\ntrain_images.shape: {}, of {}'.format(train_images.shape, train_images.dtype))
    print('test_images.shape: {}, of {}'.format(test_images.shape, test_images.dtype))

    data = json.dumps({"signature_name": "serving_default", "instances": test_images[0].tolist()})
    print("here's a test to send...")
    print(data)

    pickle.dump( train_images, open( "/mnt/train_images", "wb" ), pickle.HIGHEST_PROTOCOL )
    pickle.dump( test_images, open( "/mnt/test_images", "wb" ), pickle.HIGHEST_PROTOCOL )