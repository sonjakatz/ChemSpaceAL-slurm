#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --mem=14G
#SBATCH -p short
#SBATCH --gres=gpu:1
#SBATCH -t 24:00:00
#SBATCH -o /trinity/home/skatz/PROJECTS/ChemSpaceAL-slurm/logs/out_%j.log
#SBATCH -e /trinity/home/skatz/PROJECTS/ChemSpaceAL-slurm/logs/error_%j.log



source "/tmp/${SLURM_JOB_USER}.${SLURM_JOB_ID}/prolog.env"  # this is in tutorial script -- what does it do?

# ACTIVATE ANACONDAi
eval "$(conda shell.bash hook)"
source activate env_chemspace_slurm_v2
echo $CONDA_DEFAULT_ENV

## Step 1: get pretrained models
# python getPreTrainedModels.py

## Step 2: try if training runs using CUDA
#python 40_docking_scoring.py
python  41_docking_scoring.py
