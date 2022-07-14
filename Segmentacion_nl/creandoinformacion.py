from soma import aims
import numpy as N
import sys,os
#import shutil
#import math
#from soma import aims
import string
import bundleTools as BT
import clusterTools as CT
from claulib import *
import time

PC='fibras'
#PC='claudio'

hemis='left';Hemis='Left';HEMIS='Left';hem='l'
#hemis='right';HEMIS='Right';Hemis='Right';hem='r'

names=rtxt('/home/fibras/Dropbox/codigo_Nicole/segmentacion_exeCR/Left/Information.txt')
bunsdir='/home/'+PC+'/Dropbox/atlasCR/bundles/'+hemis+'-hemisphere/'

textlist=[]
for i in names:
	bun=bunsdir+i
	labels1, sizes1, curves_count1=BT.getBundleNamesAndSizes(bun)
	textlist.append(i+' 	8'+' 	'+str(curves_count1))

wtxt('/home/fibras/Dropbox/codigo_Nicole/segmentacion_exeCR/Left/Informationcr.txt',textlist)


