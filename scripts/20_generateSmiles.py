import sys
import ChemSpaceAL
from ChemSpaceAL import Generation
from customFunc import initConfig
import os

OUTNAME = sys.argv[1]
os.chdir('..')
base_path = f"{os.getcwd()}/results/{OUTNAME}/"

### Load global config
config_path = f"{base_path}config.json"
config = initConfig(config_path)


print(config.al_iteration)

Generation.generate_smiles(config) # this runs generation of SMILES
Generation.characterize_generated_molecules(config) # this runs an analysis of # unique, valid, and novel molecules