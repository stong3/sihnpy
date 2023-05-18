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

@pytest.fixture
def data_imb_stats():
    """ Creating data to test the imbalance mapping statistics function. 
    """

    thickness_data = datasets.pad_imb_input()[1]

    thick_data_final = thickness_data[thickness_data['session'] == 'ses-BL00']\
        .drop(labels=['session', 'run'], axis=1)
    residual_array = imb.imbalance_mapping(thick_data_final)

    return residual_array

def test_odregression_single(data_imb):
    """ Test the ODR function in sihnpy.
    """

    individual_values, model_fit = imb.odregression_single(index=data_imb.index,
                                    x=data_imb['ctx_lh_caudalanteriorcingulate_thickness'].values,
                                    y=data_imb['ctx_lh_caudalmiddlefrontal_thickness'].values)

    assert len(individual_values) == 306, 'Wrong number of participants in the output of the ODR (should be 306)'
    assert len(individual_values.columns) == 5, 'Wrong number of variables in the model output (should be 5)'
    assert len(model_fit) == 3, 'Wrong number of objects in the model fit (should be 3)'
    assert len(model_fit.columns) == 1, 'Wrong number of columns in the model fit'

    assert math.isclose(individual_values.loc['sub-1002928', 'fitted_values'], 2.451235, rel_tol=1e-5), f"Fitted value for sub-1002928 is incorrect. Should be 2.451235 not {individual_values.loc['sub-1002928', 'fitted_values']}"
    assert math.isclose(individual_values.loc['sub-1004359', 'residuals'], -0.094694, rel_tol=1e-5), f"Residuals for sub-1004359 is incorrect. Should be -0.094694 not {individual_values.loc['sub-1004359', 'residuals']}"
    assert math.isclose(individual_values.loc['sub-9930257', 'absolute_orthogonal_distances'], 0.053522, rel_tol=1e-5), f"Absolute orthogonal distance of sub-9930257 is incorrect. Should be 0.053522 not {individual_values.loc['sub-9930257', 'absolute_orthogonal_distances']}"
    assert math.isclose(individual_values.loc['sub-9939055', 'signed_orthogonal_distances'], -0.019389, rel_tol=1e-4), f"Signed orthogonal distance for sub-9939055 is incorrect. Should be -0.019389 not {individual_values.loc['sub-9939055', 'signed_orthogonal_distances']}"

    assert math.isclose(model_fit.loc['slope', 'values'], 2.251779, rel_tol=1e-5), 'The slope from ODR is not matching expected results'
    assert math.isclose(model_fit.loc['intercept', 'values'], 0.083003, rel_tol=1e-5), 'The intercept from ODR is not matching expected results'

def test_imbalance_mapping(data_imb):
    """ Test of the imbalance mapping function
    """

    residual_array_abs = imb.imbalance_mapping(data=data_imb, type='abs')
    residual_array_sign = imb.imbalance_mapping(data=data_imb, type='sign')

    assert residual_array_abs.shape == (68, 68, 306), 'Residual array is the wrong shape.'

    assert math.isclose(residual_array_abs[:,:,1][0,2], 0.002771, rel_tol=1e-3), f"Wrong value in absolute orthogonal distance array. Should be 0.002771 not {residual_array_abs[:,:,1][0,2]}"
    assert math.isclose(residual_array_sign[:,:,1][0,2], -0.002771, rel_tol=1e-3), f'Wrong value in the signed orthogonal distance array. Should be -0.002771 not {residual_array_sign[:,:,1][0,2]}'

def test_imbalance_stats(data_imb, data_imb_stats):
    """ Test of the imbalance mapping stats function
    """

    avg_imb_by_region, avg_imb_by_person, avg_imb_by_person_by_region = imb.imbalance_stats(data_imb, data_imb_stats)

    assert avg_imb_by_region.shape == (68,1), f"Wrong shape for avg_imb_by_region. Should be (68,1), not {avg_imb_by_region.shape}"
    assert avg_imb_by_person.shape == (306,1), f"Wrong shape for avg_imb_by_person. Should be (306,1), not {avg_imb_by_person.shape}"
    assert avg_imb_by_person_by_region.shape == (306, 68), f"Wrong shape for avg_imb_by_person_by_region. Should be (306,68), not {avg_imb_by_person_by_region.shape}"

    assert math.isclose(avg_imb_by_region.loc['ctx_lh_bankssts_thickness', 'avg_imbalance_by_region'], 0.062428, rel_tol=1e-5), f"Wrong value for bankssts. Should be 0.062428, not {avg_imb_by_region.loc['ctx_lh_bankssts_thickness','avg_imbalance_by_region']}"
    assert math.isclose(avg_imb_by_person.loc['sub-9931234', 'avg_imbalance_by_person'], 0.037905, rel_tol=1e-5), f"Wrong value for sub-9931234. Should be 0.037905, not {avg_imb_by_person.loc['sub-9931234','avg_imbalance_by_person']}"
    assert math.isclose(avg_imb_by_person_by_region.loc['sub-9909448', 'ctx_lh_caudalmiddlefrontal_thickness'], 0.036766, rel_tol=1e-5), f"Wrong value for sub-9909448. Should be 0.036766, not {avg_imb_by_person_by_region.loc['sub-9909448', 'ctx_lh_caudalmiddlefrontal_thickness']}"