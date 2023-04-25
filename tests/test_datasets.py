import pytest
import os
import pandas as pd
from sihnpy import datasets

def test_pad_fp_input():
    """ Function testing that the import of data is done right.
    """

    participants_data, path_ids, paths_conn = datasets.pad_fp_input()

    assert os.path.exists(path_ids), "Path to participants' ids is broken"
    assert len(participants_data)  == 15, "Wrong number of participants in participants.tsv"
    assert len(paths_conn) == 2, "Wrong number of follow-ups for dictionary"
    assert os.path.exists(paths_conn['BL00']['rest_run1']), "Paths to modalities are broken"

def test_pad_spex_input():
    """ Function testing the import of the data for the spatial extent.
    """

    tau_data, regional_averages, regional_thresholds = datasets.pad_spex_input()

    assert len(tau_data) == 308, "Wrong number of participants in the .tsv. Should be 308."
    assert tau_data['CTX_LH_ENTORHINAL_SUVR'].isnull().sum() == 0, "Some data is missing in the simulated data"
    assert len(regional_averages) == 16, "Wrong number of rows in the regional averages"
    assert len(regional_thresholds) == 16, "Wrong number of rows in the regional thresholds"

def test_pad_sw_input():
    """ Function testing the import of the data for the sliding-window
    """

    age_data = datasets.pad_sw_input()

    assert len(age_data) == 308, "Wrong number of participants in the .tsv. Should be 308."
    assert len(age_data.columns.values) == 5, "Wrong number of columns in the .tsv. Should be 4."