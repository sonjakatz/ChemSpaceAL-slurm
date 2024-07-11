import sys
import json

import ChemSpaceAL
from ChemSpaceAL import Configuration
from ChemSpaceAL import Sampling
from customFunc import initConfig

from rdkit import Chem
import shutil
import os
import pandas as pd
from tqdm import tqdm

############
from Docking_v2 import get_top_poses
###########

OUTNAME = sys.argv[1]
base_path = f"{os.getcwd()}/results/{OUTNAME}/"

### Load global config
config_path = f"{base_path}config.json"
config = initConfig(config_path)



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
print(ligand_scores)

Scoring.parse_and_prepare_diffdock_data(
    ligand_scores=ligand_scores,
    config=config
)

print("\n\n\nfinished scoring...")