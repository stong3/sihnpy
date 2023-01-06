import pytest
from sihnpy import datasets

def test_pad_conp_conn_minimal_dataset():
    """ Function testing that the import of data is done right.
    """

    participants_data, paths_conn = datasets.pad_conp_conn_minimal_dataset()

    assert len(participants_data)  == 4, "Wrong number of columns for participants.tsv"
    assert paths_conn['BL00']['rest_run1'] == '/Users/fredericst-onge/Desktop/sihnpy/src/sihnpy/data/pad_conp_minimal/BL00/rest_run1', "Dictionary not formatted correctly"