import sys
import os
import json
from customFunc import initConfig


#### Initialise global config
OUTNAME = sys.argv[1]
PROTEIN_ID = sys.argv[2]
AL_ITERATION = int(sys.argv[3])

os.chdir('..')
base_path = f"{os.getcwd()}/results/{OUTNAME}/"
config_path = f"{base_path}config.json"


dic_config = dict(
    #### init
    base_path=base_path,
    init__cycle_prefix="model7",
    init__cycle_suffix="ch1",
    init__al_iteration=AL_ITERATION,  # use 0 for pretraining
    init__training_fname="combined_train.csv.gz",
    init__validation_fname="combined_valid.csv.gz",
    init__slice_data=None,
    init__verbose=True,  # will print every important decision that's going to be made
    ####
    generation__target_criterion="force_number_filtered",
    generation__force_filter="ADMET+FGs",
    generation__target_number=1,
    ####
    ####
    sampling__n_clusters=1,      ### default: 10         
    sampling__samples_per_cluster=1,         ## default: 2  
    sampling__pca_fname="scaler_pca_combined_n120.pkl",
    ####
    scoring__protein=f"{PROTEIN_ID}.pdb",      ## 6O56
    #############
    #### Note: had to remove this part, because paths wer fucked somehow; adding this in active learning script
    #activeLearning__selection_mode="threshold",
    #activeLearning__probability_mode="linear",
    #activeLearning__threshold=11,
    #activeLearning__training_size=10,
    #activeLearning__n_replicate=None,          ### default: True
    
)



with open(config_path, 'w') as handle:
    json.dump(dic_config, handle)
