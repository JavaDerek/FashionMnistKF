from __future__ import absolute_import, division, print_function

import numpy
from minio import Minio
from minio.error import ResponseError
import sys
import os

minioClient = Minio('172.17.0.39:9000',
    access_key='AKIAIOSFODNN7EXAMPLE',
    secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    secure=False)

print('Preprocess started')
print('Instantiated Minio client')

if len(sys.argv) > 2:
    bucketNameForTrainImages =  sys.argv[1]
    bucketNameForTrainLabels = sys.argv[2]
    bucketNameForTestImages = sys.argv[3]
    bucketNameForTestLabels = sys.argv[4]
else:
    bucketNameForTrainImages =  'trainimages'
    bucketNameForTrainLabels = 'trainlabels'
    bucketNameForTestImages = 'testimages'
    bucketNameForTestLabels = 'testlabels'

print(bucketNameForTrainImages)

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

print(bucketNameForTestImages)

try:
    data = minioClient.get_object('fashionmnist', bucketNameForTestImages)
    with open('test_images', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

print('Test images retrieved from S3 to local file system')

test_images = numpy.load('test_images')

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

test_labels = numpy.load('test_labels')

print('Test labels retrieved from local file system to Numpy array')

train_images = train_images / 255.0
test_images = test_images / 255.0

numpy.save('/train_images', train_images)
numpy.save('/test_images', test_images)

try:
    with open('/train_images.npy', 'rb') as file_data:
        file_stat = os.stat('/train_images.npy')
        print(minioClient.put_object('fashionmnist', 'normalizedtrainimages',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

text_file = open("trainImagesObjectName.txt", "w")
text_file.write('normalizedtrainimages')
text_file.close()

print('Stored normalized training images in S3')

try:
    with open('/test_images.npy', 'rb') as file_data:
        file_stat = os.stat('/test_images.npy')
        print(minioClient.put_object('fashionmnist', 'normalizedtestimages',
                               file_data, file_stat.st_size))
except ResponseError as err:
    print(err)

text_file = open("testImagesObjectName.txt", "w")
text_file.write('normalizedtestimages')
text_file.close()

print('Stored normalized test images in S3')
