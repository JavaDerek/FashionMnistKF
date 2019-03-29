import tensorflow as tf
import sys
import os

from glob import glob


print("blowup started")

subfolders = glob("/*/")
for sf in subfolders:
    print(sf.replace("/",""))

print("alive")