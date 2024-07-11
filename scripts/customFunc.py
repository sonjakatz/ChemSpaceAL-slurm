import os
import sys
import json
from ChemSpaceAL import Configuration

### config_path = "/home/sonja/PROJECTS/Kiefer/ChemSpaceAL-slurm/results/test/config.json"

def initConfig(configPath):

    ''' 
    
    '''
    
    with open(configPath, "r") as f:
        dic_config = json.load(f)

    config = Configuration.Config(
        base_path=dic_config["base_path"],
        cycle_prefix=dic_config["init__cycle_prefix"],
        cycle_suffix=dic_config["init__cycle_suffix"],
        al_iteration=dic_config["init__al_iteration"],
        training_fname=dic_config["init__training_fname"],
        validation_fname=dic_config["init__validation_fname"],
        slice_data=dic_config["init__slice_data"],
        verbose=dic_config["init__verbose"]
    )
    

    ### Set path to model location
    if config.al_iteration == 0:
        config.set_training_parameters(mode="Pretraining")    
        config.set_previous_arrays()
    else: 
        ### Clarify some extra paths explicitly here
        desc_path = (
                config.pretrain_desc_path + config.training_fname.split(".")[0] + ".yaml")
        config.model_config.generation_params["desc_path"] = desc_path
        config.cycle_temp_params["path_to_al_training_set"] = os.path.join(config.al_train_path, f"{config.cycle_prefix}_al{config.al_iteration}_{config.cycle_suffix}.csv")
        config.set_training_parameters(mode="Active Learning")   
        config.set_previous_arrays()
    
    ### Generate smiles
    config.set_generation_parameters(
        target_criterion=dic_config["generation__target_criterion"], # or you could choose `force_number_unique` or `force_number_completions`
        force_filters=dic_config["generation__force_filter"], # could choose `ADMET` for no restriction on functional groups or simply remove this parameter
        target_number=dic_config["generation__target_number"])


    ### Generate sampling
    config.set_sampling_parameters(
        n_clusters=dic_config["sampling__n_clusters"], # or you could choose `force_number_unique` or `force_number_completions`
        samples_per_cluster=dic_config["sampling__samples_per_cluster"], # could choose `ADMET` for no restriction on functional groups or simply remove this parameter
        pca_fname=dic_config["sampling__pca_fname"])
    
    ### Generate scoring
    config.set_scoring_parameters(
        protein_path=dic_config["scoring__protein"]) # or you could choose `force_number_unique` or `force_number_completions`

    ### Active learning parameters
    #config.set_active_learning_parameters(
    #        selection_mode=dic_config["activeLearning__selection_mode"],
    #        probability_mode=dic_config["activeLearning__probability_mode"],
    #        threshold=dic_config["activeLearning__threshold"],
    #        training_size=dic_config["activeLearning__training_size"],
    #        n_replicate=dic_config["activeLearning__n_replicate"]
    #    )

    return config