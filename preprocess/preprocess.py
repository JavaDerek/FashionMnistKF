from __future__ import absolute_import, division, print_function

import numpy
from minio import Minio
from minio.error import ResponseError
import sys
import os
import json
import pickle

print('Preprocess started')

if (sys.argv[5] == "full"):

    minioClient = Minio('172.17.0.44:9000',
        access_key='AKIAIOSFODNN7EXAMPLE',
        secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        secure=False)

    print('Instantiated Minio client')

    bucketNameForTrainImages =  sys.argv[1]
    bucketNameForTrainLabels = sys.argv[2]
    bucketNameForTestImages = sys.argv[3]
    bucketNameForTestLabels = sys.argv[4]

    print(bucketNameForTrainImages)

    try:
        data = minioClient.get_object('fashionmnist', bucketNameForTrainImages)
        with open('train_images', 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)
    except ResponseError as err:
        print(err)

    print('Training images retrieved from S3 to local file system')

    train_images = pickle.load( open( "train_images", "rb" ) )

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

    train_labels = pickle.load( open( "train_labels", "rb" ) )

    print('Training labels retrieved from local file system to Numpy array')

    #---

    print(bucketNameForTestImages)

    try:
        data = minioClient.get_object('fashionmnist', bucketNameForTestImages)
        with open('test_images', 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)
    except ResponseError as err:
        print(err)

    print('Test images retrieved from S3 to local file system')

    test_images = pickle.load( open( "test_images", "rb" ) )

    print('Test images retrieved from local file system to Numpy array')

    #---

    print(bucketNameForTestLabels)

    try:
        data = minioClient.get_object('fashionmnist', bucketNameForTestLabels)
        with open('test_labels', 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)
    except ResponseError as err:
        print(err)

    print('Test labels retrieved from S3 to local file system')

    test_labels = pickle.load( open( "test_labels", "rb" ) )

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

    pickle.dump( train_images, open( "/train_images", "wb" ), pickle.HIGHEST_PROTOCOL )
    pickle.dump( test_images, open( "/test_images", "wb" ), pickle.HIGHEST_PROTOCOL )

    try:
        with open('/train_images', 'rb') as file_data:
            file_stat = os.stat('/train_images')
            print(minioClient.put_object('fashionmnist', 'normalizedtrainimages',
                                file_data, file_stat.st_size))
    except ResponseError as err:
        print(err)

    print('Stored normalized training images in S3')

    try:
        with open('/test_images', 'rb') as file_data:
            file_stat = os.stat('/test_images')
            print(minioClient.put_object('fashionmnist', 'normalizedtestimages',
                                file_data, file_stat.st_size))
    except ResponseError as err:
        print(err)

    print('Stored normalized test images in S3')

text_file = open("trainImagesObjectName.txt", "w")
text_file.write('normalizedtrainimages')
text_file.close()

text_file = open("testImagesObjectName.txt", "w")
text_file.write('normalizedtestimages')
text_file.close()