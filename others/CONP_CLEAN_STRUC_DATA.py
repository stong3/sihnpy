""" Structural data preparation PREVENT-AD - sihnpy

We need to clean the structural data available for sihnpy. Mostly just clean the columns and output
easy-to-use spreadsheets for users.
"""

import pandas as pd

path_to_data = "/Users/stong3/Desktop/stats_freesurfer_7.1.0"

vol_left = pd.read_csv(f"{path_to_data}/conp_pad_aparc_lh_volume.tsv", delimiter="\t")
vol_right = pd.read_csv(f"{path_to_data}/conp_pad_aparc_rh_volume.tsv", delimiter="\t")
thick_left = pd.read_csv(f"{path_to_data}/conp_pad_aparc_lh_thickness.tsv", delimiter="\t")
thick_right = pd.read_csv(f"{path_to_data}/conp_pad_aparc_rh_thickness.tsv", delimiter="\t")
aseg = pd.read_csv(f"{path_to_data}/conp_pad_aseg_volume.tsv", delimiter='\t')

vol_left_mods = (vol_left
    .assign(participant_id = vol_left['lh.aparc.volume'].str.split("_", expand=True)[0], #Breaks the first column and extract ID
            session = vol_left['lh.aparc.volume'].str.split("_", expand=True)[1], #Breaks second column and grab session
            run = vol_left['lh.aparc.volume'].str.split("_", expand=True)[2]) #Breaks third column and grab run
    .replace(to_replace={'session':{r'[NP][AR][PE]':""}}, regex=True) #Remove NAP/PRE labels
    .drop(labels=['lh.aparc.volume', 'BrainSegVolNotVent', 'eTIV'], axis=1) #Remove the old IDs, segmentation vol and TIV.
    .drop_duplicates(subset=['participant_id', 'session'], keep='last') #Removing run 01 when a run02 is available
    .set_index(['participant_id', 'session', 'run']) #Set an index
    .add_prefix('ctx_') #Add ctx_ to all columns of interest
)

vol_right_mods = (vol_right
    .assign(participant_id = vol_right['rh.aparc.volume'].str.split("_", expand=True)[0],
            session = vol_right['rh.aparc.volume'].str.split("_", expand=True)[1],
            run = vol_right['rh.aparc.volume'].str.split("_", expand=True)[2])
    .replace(to_replace={'session':{r'[NP][AR][PE]':""}}, regex=True)
    .drop(labels=['rh.aparc.volume', 'BrainSegVolNotVent', 'eTIV'], axis=1)
    .drop_duplicates(subset=['participant_id', 'session'], keep='last') #Removing run 01 when a run02 is available
    .set_index(['participant_id', 'session', 'run'])
    .add_prefix('ctx_')
)

thick_left_mods = (thick_left
    .assign(participant_id = thick_left['lh.aparc.thickness'].str.split("_", expand=True)[0], #Breaks the first column and extract ID
            session = thick_left['lh.aparc.thickness'].str.split("_", expand=True)[1], #Breaks second column and grab session
            run = thick_left['lh.aparc.thickness'].str.split("_", expand=True)[2]) #Breaks third column and grab run
    .replace(to_replace={'session':{r'[NP][AR][PE]':""}}, regex=True) #Remove NAP/PRE labels
    .drop(labels=['lh.aparc.thickness', 'lh_MeanThickness_thickness', 'BrainSegVolNotVent', 'eTIV'], axis=1) #Remove the old IDs, segmentation vol and TIV.
    .drop_duplicates(subset=['participant_id', 'session'], keep='last') #Removing run 01 when a run02 is available
    .set_index(['participant_id', 'session', 'run']) #Set an index
    .add_prefix('ctx_') #Add ctx_ to all columns of interest
)

thick_right_mods = (thick_right
    .assign(participant_id = thick_right['rh.aparc.thickness'].str.split("_", expand=True)[0], #Breaks the first column and extract ID
            session = thick_right['rh.aparc.thickness'].str.split("_", expand=True)[1], #Breaks second column and grab session
            run = thick_right['rh.aparc.thickness'].str.split("_", expand=True)[2]) #Breaks third column and grab run
    .replace(to_replace={'session':{r'[NP][AR][PE]':""}}, regex=True) #Remove NAP/PRE labels
    .drop(labels=['rh.aparc.thickness', 'rh_MeanThickness_thickness', 'BrainSegVolNotVent', 'eTIV'], axis=1) #Remove the old IDs, segmentation vol and TIV.
    .drop_duplicates(subset=['participant_id', 'session'], keep='last') #Removing run 01 when a run02 is available
    .set_index(['participant_id', 'session', 'run']) #Set an index
    .add_prefix('ctx_') #Add ctx_ to all columns of interest
)

aseg_mods = (aseg
    .assign(participant_id = aseg['Measure:volume'].str.split("_", expand=True)[0], #Breaks the first column and extract ID
            session = aseg['Measure:volume'].str.split("_", expand=True)[1], #Breaks second column and grab session
            run = aseg['Measure:volume'].str.split("_", expand=True)[2]) #Breaks third column and grab run
    .replace(to_replace={'session':{r'[NP][AR][PE]':""}}, regex=True) #Remove NAP/PRE labels
    .drop_duplicates(subset=['participant_id', 'session'], keep='last') #Removing run 01 when a run02 is available
    .set_index(['participant_id', 'session', 'run'])
    .drop(labels=['Measure:volume'], axis=1)
)

vol_left_mods.reset_index().duplicated(subset=['participant_id', 'session']).sum()
vol_left_mods.reset_index()[vol_left_mods.reset_index().duplicated(subset=['participant_id', 'session'], keep=False)]

### Next, merge left and right hemisphere together for each of volume and thickness

volume_merged = vol_left_mods.merge(vol_right_mods, left_index=True, right_index=True, how='inner')
thickness_merged = thick_left_mods.merge(thick_right_mods, left_index=True, right_index=True, how='inner')

### For now, no more modification is needed. We will leave all participants in and leave the users to decide if they want to keep
### all specific sessions or no.

volume_merged.to_csv("/Users/stong3/Desktop/sihnpy/src/sihnpy/data/conp_fsv7_1_0_volume.csv")
thickness_merged.to_csv("/Users/stong3/Desktop/sihnpy/src/sihnpy/data/conp_fsv7_1_0_thickness.csv")
aseg_mods.to_csv('/Users/stong3/Desktop/sihnpy/src/sihnpy/data/conp_fsv7_1_0_aseg.csv')