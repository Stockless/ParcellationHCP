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

def change_name(file,dict_name):
    file_name = file.split('_')
    aux = file_name[-1]
    file_name.pop()
    file_name = file_name + aux.split('.')
    # print(file_name)
    flag = False
    if "LEFT" in file_name:
        file_name.remove("LEFT")
        file_name[-1] = "."+file_name[-1]
        file_name[0] += "_lh_"
        file_name = file_name[0] + "_".join(file_name[1:-1]) + file_name[-1]
        flag = True
    if "RIGHT" in file_name:
        file_name.remove("RIGHT")
        file_name[-1] = "."+file_name[-1]
        file_name[0] += "_rh_"
        file_name = file_name[0] + "_".join(file_name[1:-1]) + file_name[-1]
        flag = True
    if flag:
        print("new: "+file_name)
        dict_name[file_name] = dict_name.pop(file)
    return dict_name

#%%
#PARA HEMISFERIO DERECHO
prev_info = open(sys.argv[1],'r') # atlas_info.txt -- para asignar umbrales correctamente
names = {}
for line in prev_info.readlines():
    line = line.split()
    # print(line)
    names[line[0]+'.bundles'] = line[1]
    if 'LEFT' in line[0] or 'RIGHT' in line[0]:
        print(line[0])
        names = change_name(line[0]+'.bundles',names)
prev_info.close()

print(names.keys())

f = open('atlas/new_atlas_info.txt', 'w')
# bundles = [s for s in os.listdir('atlas/bundles') if s.endswith('.bundles')]
for bun in os.listdir('atlas/bundles'):
    print(bun)
    if bun.endswith('.bundles'):
        atlas_bun = BT.read_bundle('atlas/bundles/'+bun)
        umbral = names[bun]
        f.write(bun.split('.')[0]+"\t"+str(umbral)+"\t"+str(len(atlas_bun))+"\n")
f.close()



