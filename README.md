## From Coarse to Fine-Grained Parcellation Refactored
This repo contains a refactoring of the work developed in the paper [From Coarse to Fine-Grained Parcellation of the Cortical Surface Using a Fiber-Bundle Atlas](https://www.frontiersin.org/articles/10.3389/fninf.2020.00032/full).

For further details, please refer to the original paper.
//![fs](/imgParcellation/fs_atlas5.png)


## Usage

The code is developed to work with tractography data from the ARCHI database. The data can be downloaded from [here](https://www.frontiersin.org/articles/10.3389/fninf.2020.00032/full).




#### ************************** Pipeline **********************************
  
Configuration settings. These files are: bv_maker.cfg y .bashrc.

1. Merge tractography files.
  - Go to 1-merge folder and run the following command:
    `python merge.py arg1`
    where arg1 is the path to the folder containing the tractography files.
  - The tractography files are merged into one .bundles file and one .bundlesdata file.
2. Resample tractography files to 21 points.

3. Transform tractography files to Talairach space.

4. Segment the tractography files.

5. Align fibers of the segmented tractographies.

6. Obtain inverse apphine transform matrix from Talairach to T1 space.

7. Intersect the segmented tractographies with the cortical mesh.

8. Filter the intersection files.

9. Parcellate:
