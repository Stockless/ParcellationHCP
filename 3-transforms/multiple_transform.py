import subprocess as sp
import sys
import os
import shutil

if len(sys.argv) <= 4:
    print("Usage: multiple_transform.py ../subjects_dir/ old/trac_folder/in/subject_dir output_folder/ input_matrix.trm")
    sys.exit(1)
subjs_dir = sys.argv[1]
old_trac_folder = sys.argv[2]
output_folder = sys.argv[3]
input_matrix = sys.argv[4] # e.g: T2_to_Tal_trm.trm
clean = input("Clean old resampled files? (y/n): ").capitalize()
sp.call(['g++', '-std=c++14', '-O3', 'transform.cpp', '-o', 'transform', '-fopenmp', '-ffast-math'])
for sub in os.listdir(subjs_dir):
    print("Transforming subject: "+sub)
    subj_bundle = subjs_dir+"/"+sub+"/"+old_trac_folder+"/"
    output = subjs_dir+"/"+sub+"/"+output_folder
    trm_matrix = subjs_dir+"/"+sub+"/TransformMatrices/"+input_matrix
    sp.call(['./transform', subj_bundle, output+'/', trm_matrix]);
    if clean[0] == 'Y':
        shutil.rmtree(subj_bundle)