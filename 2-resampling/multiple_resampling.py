import subprocess as sp
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python multiple_transform.py ../subjects_dir/")
    sys.exit(1)
subjs_dir = sys.argv[1]
clean = input("Remove oversampled fibers bundle after resampling? (y/n): ").capitalize()
sp.call(['gcc','BundleTools_sp.c', 'resampling.c', '-o', 'main', '-lm'])
for sub in os.listdir(subjs_dir):
    print("Resampling subject: "+sub)
    subj_bundle = subjs_dir+"/"+sub+"/tractography-streamline-regularized-deterministic_"+sub+".bundles"
    if not os.path.exists(subjs_dir+"/"+sub+"/resampled/"):
        os.makedirs(subjs_dir+"/"+sub+"/resampled/")
    output = subjs_dir+"/"+sub+"/resampled/resampled_"+sub+".bundles"
    sp.call(['./main', subj_bundle, output, '21']);
    # For cleaning the oversampled bundle
    if clean[0] == 'Y':
        os.remove(subj_bundle)
        os.remove(subj_bundle+'data')