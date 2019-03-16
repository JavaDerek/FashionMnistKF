from __future__ import absolute_import, division, print_function

import numpy

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

train_images = numpy.load('train_images')
#numpy.save('train_labels', train_labels)
#numpy.save('test_images', test_images)
#numpy.save('test_labels', test_labels)