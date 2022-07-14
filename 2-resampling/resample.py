import subprocess as sp
import sys
import os

subjs_dir = sys.argv[1]
subs = len(os.listdir(subjs_dir))
sub = '001'
sp.call(['gcc','BundleTools_sp.c', 'resampling.c', '-o', 'main', '-lm'])
for i in range(46,subs+1):
    if i < 10:
        sub = '00' + str(i)
    else:
        sub = '0' + str(i)
    print("Resampling subject: "+sub)
    subj_bundle = subjs_dir+"/"+sub+"/tractography-streamline-regularized-deterministic_"+sub+".bundles"
    if not os.path.exists(subjs_dir+"/"+sub+"/resampled/"):
        os.makedirs(subjs_dir+"/"+sub+"/resampled/")
    output = subjs_dir+"/"+sub+"/resampled/resampled_"+sub+".bundles"
    sp.call(['./main', subj_bundle, output, '21']);
    # For cleaning the oversampled bundle
    # sp.call(['rm','-rf',subj_bundle])
    # sp.call(['rm','-rf',subj_bundle+'.data'])