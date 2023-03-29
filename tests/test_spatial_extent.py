import numpy as np
import pandas as pd
import pytest
import math

from sihnpy import spatial_extent as spex

@pytest.fixture
def data_gmm_estimation():
    """ Define the data necessary to test the gmm_estimation function
    """
    return pd.read_csv("tests/test_data/spatial_extent/tau_data.csv", index_col=0)

@pytest.fixture
def data_gmm_measures(data_gmm_estimation):
    """ Define the data necessary to test the gmm_measures function
    """

    gm_estimations, clean_data = spex.gmm_estimation(data_to_estimate=data_gmm_estimation,
                                                    fix=True)

    return gm_estimations, clean_data

@pytest.fixture
def data_gmm_probs(data_gmm_measures):
    """ Define data necessary to test the gmm_probs function
    """

    gm_estimations, clean_data = data_gmm_measures #Tuple unpacking from the previous fixture
    final_data, final_gm_estimations, gmm_measures = spex.gmm_measures(
        cleaned_data=clean_data, gm_objects=gm_estimations, fix=False)
    
    return final_data, final_gm_estimations, gmm_measures

@pytest.fixture
def data_gmm_histogram(data_gmm_probs):
    """ Define data necessary to test the gmm_histogram function. Basically, we just need
    the probabilities as we already calculate the rest.
    """

    final_data, final_gm_estimations, gmm_measures = data_gmm_probs

    probs_df = spex.gmm_probs(final_data=final_data, final_gm_estimations=final_gm_estimations, 
        fix=False)

    return final_data, gmm_measures, probs_df

@pytest.fixture
def data_apply_clean(data_gmm_histogram):
    """ Define the data necessary to test the apply_clean function.
    """
    final_data, gmm_measures, probs_df = data_gmm_histogram

    thresh_df_one = spex.gmm_threshold_deriv(final_data=final_data, probs_df=probs_df, prob_threshs=[0.5], improb=1.0)
    thresh_df_four = spex.gmm_threshold_deriv(final_data=final_data, probs_df=probs_df, prob_threshs=[0.5], improb=1.0)

    return final_data, thresh_df_one, thresh_df_four

def test_gmm_estimation_no_fix(data_gmm_estimation):
    """ Function to test the estimation of the GMM models done in sihnpy.
    """

    gm_estimations, clean_data = spex.gmm_estimation(data_to_estimate=data_gmm_estimation, 
                                                    fix=False)

    #Checks that no regions are missing
    assert len(gm_estimations) == 16, "There should be 16 regions in the estimations"
    assert len(clean_data.columns) == 16, "There should be 16 regions in the test data"

    #Check that the BIC calculated is as expected
    assert math.isclose(gm_estimations['CTX_LH_ENTORHINAL_SUVR']
                        .bic(np.sort(clean_data['CTX_LH_ENTORHINAL_SUVR'].to_numpy()).reshape(-1,1)),
                        19.050405000530777)

def test_gmm_estimation_fix(data_gmm_estimation):
    """ Function to test that, under the right conditions, fixing the GMM estimation is done
    correctly (removes the problematic region)
    """

    gm_estimations, clean_data = spex.gmm_estimation(data_to_estimate=data_gmm_estimation,
                                                    fix=True)

    #Check that the region is missing
    assert len(gm_estimations) == 15, "There should be 15 regions after fixing"
    assert len(clean_data.columns) == 15, "There should be 15 regions in the test data after fixing"

def test_gmm_measures_no_fix(data_gmm_measures):
    """ Test that the output of the gmm_measures function works properly.
    """

    gm_estimations, clean_data = data_gmm_measures

    final_data, final_gm_estimations, gmm_measures = spex.gmm_measures(
        cleaned_data=clean_data, gm_objects=gm_estimations, fix=False)

    #Check the data organization
    assert len(final_data.columns) == 15, "Wrong number of columns in input data"
    assert len(final_gm_estimations) == 15, "Wrong number of GMM estimation in input data"

    #Check values of averages are the same
    assert math.isclose(gmm_measures['CTX_LH_ENTORHINAL_SUVR']['mean_comp1'], 1.107276418020098)

def test_gmm_measures_fix(data_gmm_measures):
    """ Test that the fix of the gmm_measures function will yield the properly fixed output.
    """

    gm_estimations, clean_data = data_gmm_measures

    final_data, final_gm_estimations, gmm_measures = spex.gmm_measures(
        cleaned_data=clean_data, gm_objects=gm_estimations, fix=True)

    assert len(final_data.columns) == 14, "Wrong number of columns in output data after fix"
    assert len(final_gm_estimations) == 14, "Wrong number of GMM estimation after fix"

def test_gmm_probs_no_fix(data_gmm_probs):
    """ Test that the probabilities are extracted normally from the function
    """
    final_data, final_gm_estimations, gmm_measures = data_gmm_probs

    probs_df = spex.gmm_probs(final_data=final_data, final_gm_estimations=final_gm_estimations, fix=False)

    assert len(probs_df.columns) == 15, "Wrong number of columns in final probability dataset"
    assert math.isclose(probs_df.loc['sub-6788676', "CTX_LH_ENTORHINAL_SUVR"], 0.13785555772799488)

    #Check the one column where we know there is an inversion
    assert math.isclose(probs_df.loc['sub-6788676', 'CTX_RH_PRECENTRAL_SUVR'], 0.0006650810571994758)

def test_gmm_probs_fix(data_gmm_probs):
    """ Test that the probabilities are fixed when the fix option is selected
    """
    final_data, final_gm_estimations, gmm_measures = data_gmm_probs

    probs_df = spex.gmm_probs(final_data=final_data, final_gm_estimations=final_gm_estimations, fix=True)
    assert len(probs_df.columns) == 15, "Wrong number of columns in final probability dataset"
    assert math.isclose(probs_df.loc['sub-6788676', "CTX_LH_ENTORHINAL_SUVR"], 0.13785555772799488)

    #Check the one column where we know there is an inversion, to make sure we grab the right
    # inverted value
    assert math.isclose(probs_df.loc['sub-6788676', "CTX_RH_PRECENTRAL_SUVR"], 0.999334918942800)

def test_gmm_histograms(data_gmm_histogram):
    """ Test that the histograms generate the right number of graphs for each category.
    """
    final_data, gmm_measures, probs_df = data_gmm_histogram

    dict_fig_density = spex.gmm_histograms(final_data=final_data, gmm_measures=gmm_measures, probs_df=probs_df, type="density")
    dict_fig_raw = spex.gmm_histograms(final_data=final_data, gmm_measures=gmm_measures, probs_df=probs_df, type="raw")
    dict_fig_probability = spex.gmm_histograms(final_data=final_data, gmm_measures=gmm_measures, probs_df=probs_df, type="probs")
    dict_fig_all = spex.gmm_histograms(final_data=final_data, gmm_measures=gmm_measures, probs_df=probs_df, type="all")

    assert len(dict_fig_density) == 15, "Wrong number of density graphs"
    assert len(dict_fig_raw) == 15, "Wrong number of raw data graphs"
    assert len(dict_fig_probability) == 15, "Wrong number of probability graphs"
    assert len(dict_fig_all) == 45, "Wrong number of graphs (all)"

def test_gmm_threshold_one_deriv_no_fix(data_gmm_histogram):
    """ Test of the threshold derivation, not fixing for improbability
    """
    final_data, gmm_measures, probs_df = data_gmm_histogram #Unpack data

    thresh_df = spex.gmm_threshold_deriv(final_data=final_data, probs_df=probs_df, prob_threshs=[0.5])

    assert len(thresh_df) == 15, "Wrong number of regions in the threshold data"
    assert len(thresh_df.columns) == 1, "Wrong number of thresholds (should be 1)"
    assert math.isclose(thresh_df.loc['CTX_LH_ENTORHINAL_SUVR', "thresh_0.5"], 1.338934852198972), "Threshold for 0.5 (left entorhinal)doesn't match expected value"
    assert math.isclose(thresh_df.loc['CTX_LH_INFERIORTEMPORAL_SUVR', "thresh_0.5"], 0.762054823679434), "Threshold for 0.5 (left inferior temporal) doesn't return the 'unfixed' value"

def test_gmm_threshold_four_deriv_no_fix(data_gmm_histogram):
    """ Test of the threshold derivation, changing the number of thresholds
    """
    final_data, gmm_measures, probs_df = data_gmm_histogram #Unpack data

    thresh_df = spex.gmm_threshold_deriv(final_data=final_data, probs_df=probs_df, prob_threshs=[0.5, 0.7, 0.8, 0.9])

    assert len(thresh_df) == 15, "Wrong number of regions in the threshold data"
    assert len(thresh_df.columns) == 4, "Wrong number of thresholds (should be 1)"

def test_gmm_threshold_deriv_fix(data_gmm_histogram):
    """ Test of the threshold derivation, fixing for improbability
    """
    final_data, gmm_measures, probs_df = data_gmm_histogram #Unpack data

    thresh_df = spex.gmm_threshold_deriv(final_data=final_data, probs_df=probs_df, prob_threshs=[0.5], improb=1.0)

    assert math.isclose(thresh_df.loc['CTX_LH_INFERIORTEMPORAL_SUVR', "thresh_0.5"], 1.5228336686419313), "Threshold for 0.5 (left inferior temporal) is not giving expected value after fix"

def test_apply_clean(data_apply_clean):
    """ Test of the apply clean function.
    """
    final_data, thresh_df_one, thresh_df_four = data_apply_clean

    data_to_apply_one, thresh_data_one = spex.apply_clean(data_to_apply=final_data, thresh_data=thresh_df_one)
    data_to_apply_four, thresh_data_four = spex.apply_clean(data_to_apply=final_data, thresh_data=thresh_df_four)

    assert len(thresh_data_one) != len(data_to_apply_one.columns), "Wrong number of regions after cleaning (1 thresh)"
    assert len(thresh_data_four) != len(data_to_apply_four.columns), "Wrong number of regions after cleaning (4 thresh)"

    assert thresh_data_one.index.values == data_to_apply_one.columns.values, "Regions' order don't match between threshold and data"