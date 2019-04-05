#/bin/bash

echo "download"
cd download
./build.sh
cd ..

echo "preprocess"
cd preprocess
./build.sh
cd ..

echo "train"
cd train
./build.sh
cd ..

echo "evaluate"
cd evaluate
./build.sh
cd ..

echo "tfsbase"
cd tfsbase
./build.sh
cd ..

python3 kfp_fashion_mnist.py kfpfmn.tar.gz
python3 short_run.py sr.tar.gz