from importlib import resources
import pandas as pd

def pad_fp_input():
    """Loads paths to functional connectivity data from a subset of 15 participants of the
    Prevent-AD open data ready for the fingerprinting analysis.

    The dataset contains functional connectivity matrices from three tasks:
    resting state, memory encoding and memory retrieval. 

    The data was taken from two timepoints:
    at baseline and 12 months later.

    Returns
    -------
    pandas.DataFrame, str, dict
        Returns, in order, a pandas.DataFrame with the participants information from the dataset,
        a path to file where this DataFrame was imported from and a dictionary of paths to
        individual connectivity matrices for each timepoint.
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

def pad_spex_input():
    """Loads the spreadsheets for the simulated tau-PET data for the 308 PREVENT-AD participants
    available in the Open dataset. This data is used to test and practice the spatial extent
    module.

    Note that all tau-PET data is **simulated** (i.e., was randomly generated and assigned to a
    participant). As such, the data should only be used for educational purposes.

    Returns
    -------
    pandas.DataFrame
        Returns three dataframes: the simulated tau-PET data for the 308 participants, a dataframe
        containing pre-computed thresholds (3SD from negative participants) and a dataframe with
        the averages and SDs used to simulate the data.
    """
    
    with resources.files('sihnpy.data.spatial_extent') as f:
        tau_data = pd.read_csv(f'{str(f)}/conp_simulated_tau-PET_data.csv').set_index('participant_id')
        regional_averages = pd.read_csv(f'{str(f)}/regional_averages.csv').set_index("region")
        regional_thresholds = pd.read_csv(f'{str(f)}/regional_thresholds.csv').set_index('region')

    return tau_data, regional_thresholds, regional_averages

def pad_sw_input():
    """ Loads the spreadsheet for the simulated age data for the 308 PREVENT-AD participants
    available in the Open dataset. This data is used to test and practice the sliding-window
    module.

    Note that all age data is **simulated** (i.e., was randomly generated and assigned to a
    participant). As such, the data should only be used for educational purposes.

    Returns
    -------
    pandas.DataFrame
        Returns a pandas DataFrame containing the simulated age of 308 participants from the 
        PREVENT-AD.
    """

    with resources.files('sihnpy.data.sliding_window') as f:
        age_data = pd.read_csv(f'{str(f)}/conp_simulated_age_data.csv').set_index('participant_id')

    return age_data