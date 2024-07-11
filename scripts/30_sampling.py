import sys
import os
import ChemSpaceAL
from ChemSpaceAL import Configuration
from ChemSpaceAL import Sampling
from customFunc import initConfig

OUTNAME = sys.argv[1]

os.chdir('..')
base_path = f"{os.getcwd()}/results/{OUTNAME}/"

### Load global config
config_path = f"{base_path}config.json"
config = initConfig(config_path)


### Do sampling
Sampling.calculate_descriptors(config)
mols = Sampling.project_into_pca_space(config)
Sampling.cluster_and_sample(mols=mols, config=config, n_iter=1)