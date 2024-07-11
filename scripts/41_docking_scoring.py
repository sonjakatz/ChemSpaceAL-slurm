import ChemSpaceAL
from ChemSpaceAL import Configuration
from ChemSpaceAL import Sampling

from rdkit import Chem
import shutil
import os
import pandas as pd
from tqdm import tqdm

############
from Docking_v2 import get_top_poses
###########

import json

### Load global config
config_path = "/trinity/home/skatz/PROJECTS/ChemSpaceAL-slurm/results/test/config.json"

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


### Set path to model location
if config.al_iteration == 0:
    config.set_training_parameters(mode="Pretraining")    
else: config.set_training_parameters(mode="Active Learning")   

### Generate smiles
config.set_generation_parameters(
    target_criterion="force_number_filtered", # or you could choose `force_number_unique` or `force_number_completions`
    force_filters="ADMET+FGs", # could choose `ADMET` for no restriction on functional groups or simply remove this parameter
    target_number=1,
)

print("\n\n\n1v")

### Sampling config
config.set_sampling_parameters(
    n_clusters=10,
    samples_per_cluster=2,
    pca_fname="scaler_pca_combined_n120.pkl",
)

### Set protein
config.set_scoring_parameters(
    protein_path="6O56.pdb",
)

print("\n\n\ntrying to get poses...")

### Dock
print(os.getcwd())

from Docking_v2 import get_top_poses
get_top_poses(
    ligands_csv=config.cycle_temp_params["path_to_sampled"],
    protein_pdb_path=config.cycle_temp_params["path_to_protein"],
    save_pose_path=config.cycle_temp_params["path_to_poses"]
)

print("\n\n\ntrying to score...")

### SCcore
from ChemSpaceAL import Scoring
ligand_scores = Scoring.score_ligands(config)

Scoring.parse_and_prepare_diffdock_data(
    ligand_scores=ligand_scores,
    config=config
)
