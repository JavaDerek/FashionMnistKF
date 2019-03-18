#/bin/bash

cd download
./build.sh
cd ..

cd preprocess
./build.sh
cd ..

cd train
./build.sh
cd ..

cd evaluate
./build.sh
cd ..

python3 kfp_fashion_mnist.py kfpfmn.tar.gz