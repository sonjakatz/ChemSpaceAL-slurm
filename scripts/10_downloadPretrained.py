import sys
import subprocess
import os

OUTNAME = sys.argv[1]
os.chdir('..')
base_path = f"{os.getcwd()}/results/{OUTNAME}/"

#@title Download (if you want) dataset/weights
#@markdown note these files will be placed into appropriate folders created above
downloadDataset = True # @param {type:"boolean"}
downloadModelWeights = True # @param {type:"boolean"}
downloadPCAweights = True # @param {type:"boolean"}
script = '''#!/bin/bash
'''
remote_source = "https://files.ischemist.com/ChemSpaceAL/publication_runs/"
if downloadDataset:
  f1 = "1_Pretraining/datasets/combined_train.csv.gz"
  f2 = "1_Pretraining/datasets/combined_valid.csv.gz"
  script += f"curl -o {base_path}{f1} {remote_source}{f1}\n"
  script += f"curl -o {base_path}{f2} {remote_source}{f2}\n"
if downloadModelWeights:
  f1 = "1_Pretraining/datasets_descriptors/combined_train.yaml"
  f2 = "1_Pretraining/model_weights/model7_al0_ch1.pt"
  script += f"curl -o {base_path}{f1} {remote_source}{f1}\n"
  script += f"curl -o {base_path}{f2} {remote_source}{f2}\n"
if downloadPCAweights:
  f1 = "3_Sampling/pca_weights/scaler_pca_combined_n120.pkl"
  script += f"curl -o {base_path}{f1} {remote_source}{f1}\n"
with open(f"{base_path}downloadPretrained.bash", "w") as f:
  f.write(script)

print("Downloading models...")
print(f"{base_path}downloadPretrained.bash")
subprocess.run(["bash",f"{base_path}downloadPretrained.bash"])