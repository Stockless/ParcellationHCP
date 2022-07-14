"""
===================================
Segmentation C algorithm
===================================
"""
# Author: Nini
# It doesn't apply neither T1 Transf. and Talairach Transf.

print(__doc__)

# ------------------------------------ Imports -----------------------------------------
from subprocess import call
import string
import re
# ------------------------- Arguments to modify by user -------------------------------
for i in ['3M','2M','1M','500k']:#['1dot5M','100k','300k','500k','1M']:
	# Directory of subject dataset to segment (.bundles)
	#subjectFileDirectory = '/media/fibras2/Disco4T/nuevastractografiasDSI/whole_brain_MNI_'+i+'z_21p.bundles'
	subjectFileDirectory = '/home/fibras2/HCP1200/100206/IN/'+i+'sift_t_MNI_21p.bundles'	
	# Directory of subject dataset to segment (.bundles)
	subjectName = '100206'

	# Directory of subject dataset to segment (.bundles)
	atlasDirectory = '/home/fibras2/test/atlas_faisceaux_MNI'

	# Erase and create a new output directory
	#ouputWorkDirectory = '/home/fibras2/HCP1200/100206/preproc/100206/T1w/Diffusion/bundles/'+i+'z/atlas_faisceaux_MNI_segmentation'
	ouputWorkDirectory = '/home/fibras2/HCP1200/100206/IN/Segment/'+i+'/DWM_seg'
	call (['rm','-rf', ouputWorkDirectory])
	call (['mkdir','-p', ouputWorkDirectory])

	# Erase and create a new output directory
	bundlesSelection = ['atlas_AR_ANT_LEFT_MNI.bundles', 
			    'atlas_AR_LEFT_MNI.bundles',
			    'atlas_AR_POST_LEFT_MNI.bundles',
			    'atlas_CG_LEFT_MNI.bundles',
			    'atlas_CG3_LEFT_MNI.bundles',
			    'atlas_CG2_LEFT_MNI.bundles',
			    'atlas_CST_LEFT_MNI.bundles',
			    'atlas_FORNIX_LEFT_MNI.bundles',
			    'atlas_IFO_LEFT_MNI.bundles',
			    'atlas_IL_LEFT_MNI.bundles',
			    'atlas_UN_LEFT_MNI.bundles',
				'atlas_THAL_FRONT_LEFT.bundles',
				'atlas_THAL_MOT_LEFT.bundles',
				'atlas_THAL_OCC_LEFT.bundles',
				'atlas_THAL_PAR_LEFT.bundles',
				'atlas_THAL_TEMP_LEFT.bundles',
	

			    'atlas_AR_ANT_RIGHT_MNI.bundles',
			    'atlas_AR_RIGHT_MNI.bundles',
			    'atlas_AR_POST_RIGHT_MNI.bundles',
			    'atlas_CG_RIGHT_MNI.bundles',
			    'atlas_CG3_RIGHT_MNI.bundles',
			    'atlas_CG2_RIGHT_MNI.bundles',
			    'atlas_CST_RIGHT_MNI.bundles',
			    'atlas_FORNIX_RIGHT_MNI.bundles',
			    'atlas_IFO_RIGHT_MNI.bundles',
			    'atlas_IL_RIGHT_MNI.bundles',
			    'atlas_UN_RIGHT_MNI.bundles',
				'atlas_THAL_FRONT_RIGHT.bundles',
				'atlas_THAL_MOT_RIGHT.bundles',
				'atlas_THAL_OCC_RIGHT.bundles',
				'atlas_THAL_PAR_RIGHT.bundles',
				'atlas_THAL_TEMP_RIGHT.bundles',


	 		    'atlas_CC_ROSTRUM_MNI.bundles',    		
			    'atlas_CC_SPLENIUM_MNI.bundles',   			
			    'atlas_CC_GENU_MNI.bundles',       		
			    'atlas_CC_BODY_MNI.bundles']

	# -------------------------- Get parameter from txt file --------------------------------
	# Get the labels, thresolds and amount of fiber for each bundle to analize

	# Setting arguments for execution 
	arg = ['./Segmentation', subjectFileDirectory, subjectName, atlasDirectory, ouputWorkDirectory]

	for bundle in bundlesSelection:     
	    arg.append(bundle)

	# ---------------------------- Execute C code to get bundles ---------------------------
	# Executing C code
	print arg
	print "... ... ... Executing C code ... ... ..."
	call (arg)



