
## Authors:  
    Narciso López López
    Andrea Vázquez Varela
Last modification: 24-10-2018

C code for resampling fibers of a bundle to N points
Python code for aligning the fibers of the bundles as them can be dissaligned on their ends within its bundles

# Python modules
- dipy
- numpy

# Compile: 
g++ -std=c++14 -O3 main.cpp -o main -fopenmp -ffast-math

# Execute:
./main resample_points tractography.bundles subject_number path/to/atlas path/to/atlas_info.txt results_folder
Example: ./main 21 Data/subs/001/tractography-filtered.bundles 001 atlas/bundles atlas/atlas_info.txt resampled_output

Once resampled run the align_bundles.py for bundle fibers alignment
python align_bundles.py 

# Cite: 

@inproceedings{vazquez2019parallel,
  title={Parallel Optimization of Fiber Bundle Segmentation for Massive Tractography Datasets},
  author={V{\'a}zquez, Andrea and L{\'o}pez-L{\'o}pez, Narciso and Labra, Nicole and Figueroa, Miguel and Poupon, Cyril and Mangin, Jean-Fran{\c{c}}ois and Hern{\'a}ndez, Cecilia and Guevara, Pamela},
  booktitle={2019 IEEE 16th International Symposium on Biomedical Imaging (ISBI 2019)},
  pages={178--181},
  year={2019},
  organization={IEEE}
}
