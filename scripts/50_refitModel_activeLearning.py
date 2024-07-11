import sys
import json
import subprocess
import os

import ChemSpaceAL
from ChemSpaceAL import Dataset, Model, Training, ALConstruction
from customFunc import initConfig


print("\n\n\n Starinting to do active learning... \n\n\n\n")

OUTNAME = sys.argv[1]
PROTEIN_ID = sys.argv[2]
''' optional arguments to add here maybe: training set size, custom threshold,... '''

os.chdir('..')
base_path = f"{os.getcwd()}/results/{OUTNAME}/"

### Load global config
config_path = f"{base_path}config.json"
config = initConfig(config_path)



## add `active_learning_parameters` here and not in config.json because otherwise paths are somehow fucked 
config.set_active_learning_parameters(
    selection_mode="threshold", probability_mode="linear", threshold=11, training_size=10, n_replicate=False)

### Construct new training set & load
''' 
If there is a timeout on the cluster, it will fail here (due to `do_sampling=True`, but wont give an error message, it will simply be stuck)
'''
ALConstruction.construct_al_training_set(config=config, do_sampling=True)


'''
manually increment al_iteration count by 1 here so paths are ok?

works for iteration 0 --> 1 but have to test for others as well
'''
AL_ITERATION_next = config.al_iteration+1
config.al_iteration = AL_ITERATION_next


### Load constructed dataset
'''
Note: 
I am confused about the set paths here... because this function is coded to use the !previous! al_iteration as training set. 
Similar as in their official collab (section Active Learning) the original paths are: 
    - "the training set will be saved to             5_ActiveLearning/training_sets/model0_al1_ch1.csv" 
    ...
    - "Will load AL training set from 5_ActiveLearning/training_sets/model0_al0_ch1.csv"

I think this is stupid / I dont understand it so I tried to make this consistent with the code in line 34 above, but keep an eye out for inconsistencies; 
Now in our version: 
    - the training set will be saved to             5_ActiveLearning/training_sets/model7_al0_ch1.csv
    ...
    - Will load AL training set from 5_ActiveLearning/training_sets/model7_al0_ch1.csv
'''
al_ds = Dataset.load_data(config=config, mode="Active Learning")
config.set_training_parameters(mode="Active Learning", epochs=1)

### Fine-tune model
model, trainer = Training.train_GPT(
    config=config,
    training_dataset=al_ds,
)


'''
Here we update the global config to the new, manually set al_iteration so the next iteration of training is correct
'''
os.chdir("scripts")
subprocess.run(["python", "01_initialiseConfig.py", f"{OUTNAME}", f"{PROTEIN_ID}", f"{AL_ITERATION_next}"])


