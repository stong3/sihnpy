import pandas as pd
import pytest
import math

from sihnpy import imbalance_mapping as imb
from sihnpy import datasets

@pytest.fixture
def data_imb():
    """ Importing the data to test the imbalance_mapping functions. We just import the thickness
    data and do basic cleaning.
    """

    thickness_data = datasets.pad_imb_input()[1]

    return thickness_data[thickness_data['session'] == 'ses-BL00'].drop(labels=['session', 'run'], axis=1)

def test_odregression_single(data_imb):
    """ 
    """

    individual_values, model_fit = imb.odregression_single(index=data_imb.index,
                                    x=data_imb['ctx_lh_caudalanteriorcingulate_thickness'].values,
                                    y=data_imb['ctx_lh_caudalmiddlefrontal_thickness'].values)

def test_imbalance_mapping():
    """ 
    """

def test_imbalance_stats():
    """ 
    """