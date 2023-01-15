from importlib import resources
import pandas as pd

def pad_fp_input():
    """ Loads paths to functional connectivity data from a subset of 15 participants of the
    Prevent-AD open data ready for the fingerprinting analysis.

    The dataset contains functional connectivity matrices from three tasks:
    resting state, memory encoding and memory retrieval. 

    The data was taken from two timepoints:
    at baseline and 12 months later.

    More information on the data is available here:

    """
    #Create dictionary by visit
    dict_paths = {"BL00": {}, "FU12": {}}

    #For both visits, for each fMRI modality, find the path to the matrices
    for visits in dict_paths.keys():
        for modalities in ['rest_run1', 'rest_run2', 'encoding', 'retrieval']:
            with resources.files('sihnpy.data.pad_conp_minimal') as f:
                #Update the nested dictionary with the right path to find the matrices.
                dict_paths[visits].update({modalities: f"{str(f)}/{visits}/{modalities}"})

    #Import the demographic data in a pandas DF
    with resources.files('sihnpy.data.pad_conp_minimal') as f:
        path_participant_file = f'{str(f)}/participants.tsv'
        participants = pd.read_csv(path_participant_file, delimiter="\t")

    return participants, path_participant_file, dict_paths
