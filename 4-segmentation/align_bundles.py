import os
import numpy as np
import sys
import re
from dipy.segment.metric import mdf
from dipy.segment.metric import dist
from dipy.segment.metric import EuclideanMetric

#Imports bundleTools3 from parent directory
sys.path.append('../bundleTools')
import bundleTools as bt

"""Alings fibers of a bundle """
def align_bundle(bundle, ref):
    aligned_bundle = []
    for fiber in bundle:
        d = dist(EuclideanMetric(), fiber, ref)/21
        f = mdf(fiber, ref)
        
        if f < d:
            aligned_bundle.append(fiber[::-1])
            
        else:
            aligned_bundle.append(fiber)

    return aligned_bundle

def calculate_centroid(bundle):
    return np.mean(bundle, axis = 0)

"""opens a directory and returns a list of all the files in it"""
def get_files(path):
    files = []
    for file in os.listdir(path):
        if file.endswith(".bundles"):
            files.append(file)
    return files

path = sys.argv[1] #bundles path
bundles = get_files(path)

#Creates aligned fibers folder
aligned_path = "aligned_bundles/"
if not os.path.exists(aligned_path):
    os.makedirs(aligned_path)
    

for bundle in bundles:
    start = bundle.find("lh")
    if start == -1:
        start = bundle.find("rh")
    # print(bundle[start:])
    name = "_".join(bundle[start:].split("_")) #saves the name of the regions of the bundle e.g "AR_ANT.bundles"
    bundle = bt.read_bundle(path + bundle)
    centroid = calculate_centroid(bundle)

    aligned_bundles = align_bundle(bundle, centroid)

    bt.write_bundle(aligned_path + '/aligned_' +  name, aligned_bundles)