#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --mem=14G
#SBATCH -p long
#SBATCH --gres=gpu:1
#SBATCH -t 48:00:00
#SBATCH --nodelist=gpu002
#SBATCH --output=/trinity/home/r095689/PROJECTS/ChemSpaceAL-slurm/logs/output_%j.log
#SBATCH --error=/trinity/home/r095689/PROJECTS/ChemSpaceAL-slurm/logs/error_%j.log

################
# Note on running: 
# to submit script successfully you have to chdir into "/scripts" and then `sbatch full_iteration.sh`; otherwise paths are not correct
# ...chagne this to something better in the future
################


# ACTIVATE ANACONDAi
eval "$(conda shell.bash hook)"
source activate env_chemspace
echo $CONDA_DEFAULT_ENV

OUTPUT_NAME="fullIter_3"
PROTEIN_ID="1iep"
AL_ITERATION=0

#####################
### To implement still
### if AL_iteration = 0: run from steps 0-5; else: 2-5
#####################

## Step 0a: Init Dirs
#python 00_initaliseDir.py $OUTPUT_NAME #<-- commented out for it 1 to see if it works


## Step 0b: Init Config with all settings for the run (except active learning)
#############
### To watch out: initialise config has random hardcoded variables primarily for debugging - change this in a real run!
#############
#python 01_initialiseConfig.py $OUTPUT_NAME $PROTEIN_ID $AL_ITERATION  #<-- commented out for it 1 to see if it works

## Step 0c: [OPTIONAL] Download .pdb of target protein if available in uniprot
#wget https://files.rcsb.org/download/$PROTEIN_ID.pdb -P ../results/$OUTPUT_NAME/4_Scoring/binding_targets
#if [ -z "$(ls -A "../results/$OUTPUT_NAME/4_Scoring/binding_targets")" ]; then
#    wget -P "../results/$OUTPUT_NAME/4_Scoring/binding_targets" "https://files.rcsb.org/download/$PROTEIN_ID.pdb"
#fi  # <-- commented out for it 1 to see if it works

## Step 1: get pretrained models
#python 10_downloadPretrained.py $OUTPUT_NAME  #<-- commented out for it 1 to see if it works

## Step 2: generate smiles from downloaded, pretrained models
#python 20_generateSmiles.py $OUTPUT_NAME

## Step 3: generate smiles from downloaded, pretrained models
#python 30_sampling.py $OUTPUT_NAME

## Step 4: generate smiles from downloaded, pretrained models
#python 40_docking_scoring.py $OUTPUT_NAME

## Step 5: generate new training set and refit model
python 50_refitModel_activeLearning.py $OUTPUT_NAME $PROTEIN_ID
