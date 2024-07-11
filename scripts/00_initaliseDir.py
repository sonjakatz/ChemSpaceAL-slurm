import sys
import ChemSpaceAL
from ChemSpaceAL import InitializeWorkspace
import os
import json


OUTNAME = sys.argv[1]

os.chdir('..')
base_path = f"{os.getcwd()}/results/{OUTNAME}/"
os.makedirs(base_path, exist_ok=True)

InitializeWorkspace.create_folders(base_path=base_path)

