# FashionMnistKF
A really simple, self-contained KubeFlow demo

For complete details, read my blog series on "Building a Kubeflow Pipelines demo" at https://derekmferguson.wixsite.com/ml4nonmath

Here's how to run this for yourself...

1) Get and install MiniKF from https://www.kubeflow.org/docs/started/getting-started-minikf/
2) Clone all of the code in this repository
3) Establish a personal Docker.io account at http://docker.io
4) Do a global search for "dotnetderek" and replace with the name of your personal Docker.io account
5) Do a "vagrant ssh"
6) In your new SSH window in the MiniKF virtual box, run this command to install and start up Minio...

docker run -p 9000:9000 --name minio1 -e "MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" -e "MINIO_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" -v /data/rok:/data -v /data/rok/config:/root/.minio minio/minio server /data &

7) Back on your main host computer's terminal window, run build.sh from the root of the GIT repo (note: you may need to do "chmod +x" on all of the build.sh files, first)
8) Navigate to http://10.10.10.10
9) Click "Pipeline Dashboard"
10) Click "Upload Pipeline"
11) Choose "fkpfmn.tar.gz" that was built by step #7 above - give it a friendly name you'll remember
12) Click your newly-created pipeline
13) Click "Start an experiment" and give it whatever name and description you like
14) After you save that, you'll be asked to create a first Run - give it whatever name you like and hit "Create"
15) On the page that comes up, choose the run that was just added
16) Click boxes and choose tabs on the flyout to inspect the current state of each step
17) Click "Refresh" to see boxes added as steps run

Hopefully, if everything has worked, you'll get to a point where all of the boxes have appeared and have green checks.  You're up and running!