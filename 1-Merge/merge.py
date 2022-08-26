import os
import sys
import shutil
from dipy.segment.metric import EuclideanMetric
from dipy.segment.metric import mdf
from dipy.segment.metric import dist

#Import bundleTools from parent directory
sys.path.append('../bundleTools')
import bundleTools as BT
import bundleTools3 as BT3

if len(sys.argv) < 2:
    print("Usage: python merge.py ../subjects_dir/")
    sys.exit(0)

subjects_path = sys.argv[1]+'/'
clean = input("Clean OverSampledFibers folder after merging? (y/n): ").capitalize()
subjects_list = os.listdir(subjects_path);

for subject in subjects_list:
    print("Merging subject: "+subject)
    if(subject != 'meshes_obj'):
        #Juntar 3 tractografias en un solo archivo .bundles
        all_points=[]
        fiber_bun_1_3 = subjects_path+subject+'/OverSampledFibers/tractography-streamline-regularized-deterministic_1_3.bundles'
        fiber_points_1_3 = BT.read_bundle(fiber_bun_1_3)
        for fiber in fiber_points_1_3:
            all_points.append(fiber)

        fiber_bun_2_3 = subjects_path+subject+'/OverSampledFibers//tractography-streamline-regularized-deterministic_2_3.bundles'
        fiber_points_2_3 = BT.read_bundle(fiber_bun_2_3)
        for fiber in fiber_points_2_3:
            all_points.append(fiber)

        fiber_bun_3_3 = subjects_path+subject+'/OverSampledFibers//tractography-streamline-regularized-deterministic_3_3.bundles'
        fiber_points_3_3 = BT.read_bundle(fiber_bun_3_3)
        for fiber in fiber_points_3_3:
            all_points.append(fiber)

        BT3.write_bundle(subjects_path+subject+'/tractography-streamline-regularized-deterministic_'+subject+'.bundles', all_points)
        if clean[0] == 'Y':
            shutil.rmtree(subjects_path+subject+'/OverSampledFibers/')
    # For non merged bundles
    # all_points = []
    # for file in os.listdir(subjects_path+"/"+subject+"/non_merged/"):
    #     if file.endswith(".bundles"):
    #         fiber_points = BT.read_bundle(subjects_path+"/"+subject+"/non_merged/"+file)
    #         for fiber in fiber_points:
    #             all_points.append(fiber)
    # BT3.write_bundle(subjects_path+"/"+subject+"/merged_"+subject+".bundles", all_points)