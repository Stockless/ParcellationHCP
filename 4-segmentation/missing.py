import os
"""Checks the atlas info file for the missing files over the atlas input bundles and returns a list of the missing files"""
fp = open("atlas/atlas_info.txt", "r")

#reads a directory and returns a list of all the files in it
def read_dir(dir):
    files = []
    for file in os.listdir(dir):
        files.append(file)
    return files

files = read_dir("atlas/bundles")
atl_info = []
missing = []
while True:
    line = fp.readline()
    if not line:
        break
    line = line.split()
    atl_info.append("atlas_"+line[0]+".bundlesdata")
    if "atlas_"+line[0]+".bundlesdata" not in files:
        missing.append(line[0])
    
fp.close()

print("Files on directory not in atlas_info file:")
for f in files:
    if f[-8:] == ".bundles":
        continue
    if f not in atl_info:
        print(f)
print()
print("Required files from atlas_info that are missing:")
for f in missing:
    print(f)