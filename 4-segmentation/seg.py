#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 16:21:08 2022

@author: cris
"""

import random
import os
import sys
sys.path.append('../bundleTools')
import bundleTools as BT


#%%
#PARA HEMISFERIO DERECHO
prev_info = open(sys.argv[1],'r') # atlas_info.txt -- para asignar umbrales correctamente
names = {}
for line in prev_info.readlines():
    line = line.split()
    names['atlas_'+line[0]+'.bundles'] = line[1]
prev_info.close()

f = open('atlas_2/rightInfo.txt', 'w')
bundles = [s for s in os.listdir('atlas/bundles') if s.endswith('.bundles')]
for bun in bundles:
    print(bun)
    pals = bun.split('_')
    if pals[1] == 'rh' or pals[-1].split('.')[0]=='RIGHT':
        atlas_bun = BT.read_bundle('atlas/bundles/'+bun)
        largo = names[bun]
        f.write(bun.split('.')[0]+"\t"+str(largo)+"\t"+str(len(atlas_bun))+"\n")
f.close()

