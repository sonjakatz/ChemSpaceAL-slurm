import sys
import ChemSpaceAL
from ChemSpaceAL import InitializeWorkspace
import os
import json


OUTNAME = sys.argv[1]

os.chdir('..')
base_path = f"{os.getcwd()}/results/{OUTNAME}/"

InitializeWorkspace.create_folders(base_path=base_path)

