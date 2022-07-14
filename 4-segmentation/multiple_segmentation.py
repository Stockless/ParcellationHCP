import subprocess as sp
import sys
import os

subjs_dir = sys.argv[1] #Data/subs
subs = 5#len(os.listdir(subjs_dir))
atlas_bundles = sys.argv[2] #atlas/bundles
atlas_info = sys.argv[3] #atlas/info.txt
sub = '001'
sp.call(['g++', '-std=c++14', '-O3', 'segmentation_2.cpp', '-o', 'segmentation', '-fopenmp', '-ffast-math'])
for i in range(1,subs+1):
    if i < 10:
        sub = '00' + str(i)
    else:
        sub = '0' + str(i)
    print("Segmenting subject "+sub)
    subj_bundle = subjs_dir+"/"+sub+"/transformed_Tal/resampled_"+sub+".bundles"
    output_dir = subjs_dir+"/"+sub+"/segmented_Tal"
    sp.call(['./segmentation', '21', subj_bundle, 'subject', atlas_bundles, atlas_info, output_dir])