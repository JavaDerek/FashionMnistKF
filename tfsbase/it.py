from __future__ import absolute_import, division, print_function
from flask import Flask
import numpy
from minio import Minio
from minio.error import ResponseError
import sys
import os
import tensorflow as tf

app = Flask(__name__)

@app.route('/')
def hello_world():
    minioClient = Minio('172.17.0.39:9000',
        access_key='AKIAIOSFODNN7EXAMPLE',
        secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        secure=False)
    print('Instantiated Minio client')
    bucketNameForModel = 'trainedmodel'

    try:
        data = minioClient.get_object('fashionmnist', bucketNameForModel)
        with open('model.h5', 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)
    except ResponseError as err:
        print(err)

    print('Model retrieved from S3 to local file system')

    # The export path contains the name and the version of the model
    tf.keras.backend.set_learning_phase(0)  # Ignore dropout at inference
    model = tf.keras.models.load_model('model.h5')
    export_path = '/tmp/mnist_model/1'

    # Fetch the Keras session and save the model
    # The signature definition is defined by the input and output tensors
    # And stored with the default serving key
    with tf.keras.backend.get_session() as sess:
        tf.saved_model.simple_save(
            sess,
            export_path,
            inputs={'input_image': model.input},
            outputs={t.name: t for t in model.outputs})

    return "Saved as consumable model"


if __name__ == '__main__':
    print('tfsbase started')
    app.run(debug=True, host='0.0.0.0')
