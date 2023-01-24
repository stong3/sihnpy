import pytest
import os
from sihnpy import datasets

def test_pad_fp_input():
    """ Function testing that the import of data is done right.
    """

    participants_data, path_ids, paths_conn = datasets.pad_fp_input()

    assert os.path.exists(path_ids), "Path to participants' ids is broken"
    assert len(participants_data)  == 15, "Wrong number of participants in participants.tsv"
    assert len(paths_conn) == 2, "Wrong number of follow-ups for dictionary"
    assert os.path.exists(paths_conn['BL00']['rest_run1']), "Paths to modalities are broken"