#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --mem=14G
#SBATCH -p interactive
#SBATCH --gres=gpu:1
#SBATCH -t 1:00:00
#SBATCH -o /trinity/home/skatz/PROJECTS/ChemSpaceAL-slurm/logs/out_%j.log
#SBATCH -e /trinity/home/skatz/PROJECTS/ChemSpaceAL-slurm/logs/error_%j.log

################
# Note on running: 
# to submit script successfully you have to chdir into "/scripts" and then `sbatch full_iteration.sh`; otherwise paths are not correct
# ...chagne this to something better in the future
################


# ACTIVATE ANACONDAi
eval "$(conda shell.bash hook)"
source activate env_chemspace_slurm_v2
echo $CONDA_DEFAULT_ENV

OUTPUT_NAME="fullIter_3"
PROTEIN_ID="6O56"
AL_ITERATION=0

#####################
### To implement still
### if AL_iteration = 0: run from steps 0-5; else: 2-5
#####################

## Step 0a: Init Dirs
python 00_initaliseDir.py $OUTPUT_NAME


## Step 0b: Init Config with all settings for the run (except active learning)
#############
### To watch out: initialise config has random hardcoded variables primarily for debugging - change this in a real run!
#############
python 01_initialiseConfig.py $OUTPUT_NAME $PROTEIN_ID $AL_ITERATION

## Step 0c: [OPTIONAL] Download .pdb of target protein if available in uniprot
#wget https://files.rcsb.org/download/$PROTEIN_ID.pdb -P ../results/$OUTPUT_NAME/4_Scoring/binding_targets
if [ -z "$(ls -A "../results/$OUTPUT_NAME/4_Scoring/binding_targets")" ]; then
    wget -P "../results/$OUTPUT_NAME/4_Scoring/binding_targets" "https://files.rcsb.org/download/$PROTEIN_ID.pdb"
fi

## Step 1: get pretrained models
python 10_downloadPretrained.py $OUTPUT_NAME

## Step 2: generate smiles from downloaded, pretrained models
python 20_generateSmiles.py $OUTPUT_NAME

## Step 3: generate smiles from downloaded, pretrained models
python 30_sampling.py $OUTPUT_NAME

## Step 4: generate smiles from downloaded, pretrained models
python 40_docking_scoring.py $OUTPUT_NAME

## Step 5: generate new training set and refit model
python 50_refitModel_activeLearning.py $OUTPUT_NAME $PROTEIN_ID
