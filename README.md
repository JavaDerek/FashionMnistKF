# FashionMnistKF
A really simple, self-contained KubeFlow demo

For complete details, read my blog series on "Building a Kubeflow Pipelines demo" at https://derekmferguson.wixsite.com/ml4nonmath

Here's how to run this for yourself...

Pre-requisites

* Get and install Docker from https://www.docker.com/get-started 
* Get and install MiniKF from https://www.kubeflow.org/docs/started/getting-started-minikf/
* Get and install Python 3 from https://www.python.org/downloads/ 
* Get and install the KubeFlow Pipelines library for Python 3 via "pip3 install python-dateutil https://storage.googleapis.com/ml-pipeline/release/0.1.2/kfp.tar.gz --upgrade"
* Get and install Postman from http://www.getpostman.com

Setup Process

1) Clone all of the code in this repository
2) Establish a personal Docker.io account at http://hub.docker.com
3) Do a global search for "dotnetderek" and replace with the name of your personal Docker.io account
4) Do a "vagrant ssh"
5) In your new SSH window in the MiniKF virtual box, run this command to install and start up Minio...

docker run -p 9000:9000 --name minio1 -e "MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" -e "MINIO_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" -v /data/rok:/data -v /data/rok/config:/root/.minio minio/minio server /data &

6) Note the IP that is given to you when this finishes.  Run a global replace in your IDE of choice to replace the IP 172.17.0.44 with whatever IP you saw above.

7) In the same SSH window in the MiniKF virtual box, run these commands to install and start up TensorFlow Serving...

* mkdir -p /tmp/tfserving
* cd /tmp/tfserving
* git clone https://github.com/tensorflow/serving
* docker run --mount type=bind,source="/tmp/tfserving/serving/tensorflow_serving/servables/tensorflow/testdata/saved_model_half_plus_two_cpu",target="/models/half_plus_two" -e MODEL_NAME=half_plus_two -p 8501:8501 -p 5000:5000 -t dotnetderek/tfsbase:latest &

NOTE: be aware that it is normal for your console to start spinning with error messages after this.  They will go away after we run the pipeline once to completion (by the end of these instructions).

8) Back on your main host computer's terminal window, run build.sh from the root of the GIT repo (note: you may need to do "chmod +x" on all of the build.sh files, first)
9) Navigate to http://10.10.10.10:8080 
10) Click "Pipeline Dashboard"
11) Click "Upload Pipeline"
12) Choose "fkpfmn.tar.gz" that was built by step #6 above - give it a friendly name you'll remember
13) Click your newly-created pipeline
14) Click "Create experiment" and give it whatever name and description you like
15) After you save that, you'll be asked to create a first Run - give it whatever name you like and hit "Create"
16) On the page that comes up, choose the run that was just added by clicking its name (not the checkbox)
17) Click boxes and choose tabs on the flyout to inspect the current state of each step
18) Wait until you get to a point where all of the boxes have appeared and have green checks.
19) From the "preprocess" step's Logs, copy the big JSON message that appeared underneath the line that reads "here's a test to send..."
20) Past this into the body of a POST method in Postman, with a URL of http://10.10.10.10:8501/v1/models/mnist:predict
21) When you click send, you should get back a JSON prediction -- if so... you're up-and-running!