
import os
import sys

# opens a directory and changes the name of all files in it
def change_name(dir_name):
    for file in os.listdir(dir_name):
        file_name = file.split('_')
        aux = file_name[-1]
        file_name.pop()
        file_name = file_name + aux.split('.')
        print(file_name)
        if "LEFT" in file_name:
            file_name.remove("LEFT")
            file_name[-1] = "."+file_name[-1]
            file_name[0] += "_lh_"
            file_name = file_name[0] + "_".join(file_name[1::])
        if "RIGHT" in file_name:
            file_name.remove("RIGHT")
            file_name[-1] = "."+file_name[-1]
            file_name[0] += "_rh_"
            file_name = file_name[0] + "_".join(file_name[1::])
            #os.rename(dir_name + '/' + file, dir_name + '/' + new_name)
        os.rename(dir_name + '/' + file, dir_name + '/' + file_name)

change_name("fused bundle-atlas")