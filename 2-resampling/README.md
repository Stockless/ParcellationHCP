
### Compile 
  gcc BundleTools_sp.c resampling.c -o resampling -lm

### Execute 
  ./resampling subject_tractography.bundles output_tractography.bundles points(21)
  e.g: ./resampling ../../Data/001/tractography-streamline-regularized-deterministic_001.bundles resampled-tractography_001.bundles 21

### Multiple subjects execution

  python multiple_resampling.py ../subjects/dir


### Subjects dir folder format
  Subjects dir should contain all subjects separated in folders as follow:
    - subject/dir/001
    - subject/dir/002
    - ...
    - subject/dir/xyz
    Where xyz is the number of the subject

  Also the tractography bundle of each subject should have the name:
    - tractography-streamline-regularized-deterministic_xyz.bundles
    Where xyz is the number of the subject. This should be the merged bundle and should be inside the root of the subject dir.

  This will create a folder named 'resampled' with the resampled tractography inside each subject folder.