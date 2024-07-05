import ChemSpaceAL
from ChemSpaceAL import InitializeWorkspace
from ChemSpaceAL import Configuration
from ChemSpaceAL import Dataset
from ChemSpaceAL import Model
from ChemSpaceAL import Training
from ChemSpaceAL import Generation

import json


### Load global config
config_path = "/home/sonja/PROJECTS/Kiefer/ChemSpaceAL-slurm/results/test/config.json"

with open(config_path, "r") as f:
    dic_config = json.load(f)

config = Configuration.Config(
    base_path=dic_config["base_path"],
    cycle_prefix=dic_config["cycle_prefix"],
    cycle_suffix=dic_config["cycle_suffix"],
    al_iteration=dic_config["al_iteration"],
    training_fname=dic_config["training_fname"],
    validation_fname=dic_config["validation_fname"],
    slice_data=dic_config["slice_data"],
    verbose=dic_config["verbose"]
)
config.set_previous_arrays()



### Sampling config
config.set_sampling_parameters(
    n_clusters=10,
    samples_per_cluster=2,
    pca_fname="scaler_pca_combined_n120.pkl",
)


### Do sampling
Sampling.calculate_descriptors(config)
mols = Sampling.project_into_pca_space(config)
Sampling.cluster_and_sample(mols=mols, config=config, n_iter=1)