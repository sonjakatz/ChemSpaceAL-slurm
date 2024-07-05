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

Generation.generate_smiles(config) # this runs generation of SMILES
Generation.characterize_generated_molecules(config) # this runs an analysis of # unique, valid, and novel molecules