import os
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from scipy import stats
from matplotlib import pyplot as plt

def gmm_estimation(data_to_estimate, fix=False):
    """ Function estimating a 1- and a 2-cluster solution Gaussian Mixture Model. The Bayesian
    Information Criteria is output and compared between the two models.
    """

    data = data_to_estimate.copy()
    gm_objects = {}
    col_rem_id = []

    for col in data_to_estimate:
        print(f'GMM estimation for {col}')

        #For each column, sort the dataframe from lowest to highest and convert to 1D np.ndarray
        sorted_df = data.sort_values(by=col)
        roi_suvr = sorted_df[col].to_numpy().reshape(-1,1)

        #Estimate the GMM models
        gm1 = GaussianMixture(n_components=1, random_state=667).fit(roi_suvr)
        gm2 = GaussianMixture(n_components=2, random_state=667).fit(roi_suvr)

        print(f"1-component: {gm1.bic(roi_suvr)} | 2-components: {gm2.bic(roi_suvr)} ")

        #Store GMM estimation object
        gm_objects[col] = gm2

        #In the case that 1 distribution works better, here are the options
        if gm1.bic(roi_suvr) <= gm2.bic(roi_suvr):
            print("GMM estimation suggests that 1 component is a better fit to the data")

            #If we want to remove the column with 1 component, save the ID here.
            if fix is True:
                print(f"-Fix is True: Region {col} will be removed from further calculation")
                col_rem_id.append(col)
                del gm_objects[col]
            else:
                print(f"-Fix is False: Region {col} will be kept in the data")

    #Remove columns, if errors in estimation AND fix is true
    clean_data = data.drop(col_rem_id, axis=1)

    return gm_objects, clean_data

def _gmm_avg_sd(col, gm_obj):
    """ Quick function extracting and returning the average and SD values of the two components.
    """
    dict_gmm_measures = {}

    dict_gmm_measures[f'mean_comp1_{col}'] = gm_obj.means_[0][0]
    dict_gmm_measures[f'mean_comp2_{col}'] = gm_obj.means_[1][0]
    dict_gmm_measures[f'sd_comp1_{col}'] = np.sqrt(gm_obj.covariances_[0][0])[0]
    dict_gmm_measures[f'sd_comp2_{col}'] = np.sqrt(gm_obj.covariances_[1][0])[0]

    return dict_gmm_measures

def gmm_measures(cleaned_data, gm_objects, fix=False):
    """ For all data kept after GMM estimation, compute the averages and SDs for both components.
    We then check that the order of the clusters is right and the measures are also used for
    the histograms.

    Finally, we compute the probabilities of belonging to the second cluster for each region. We
    will save that probability for the threshold determination.
    """

    tmp_df = cleaned_data.copy() #To avoid modifying the input.
    final_dict = gm_objects.copy() #To avoid modifying the input
    rem_cols = [] #For fixing if needed
    gmm_measures = {} #To store the GMM averages and SDs for histograms

    for col, gm_obj in final_dict.items():
        #Return averages and SDs of the components
        gmm_measures[col] = _gmm_avg_sd(col, gm_obj)

        #Check that average of second component is higher than the first component 
        if gmm_measures[col][f'mean_comp1_{col}'] > gmm_measures[col][f'mean_comp2_{col}']:
            print(f"Average of first component of {col} is higher than second component.")

            if fix is True:
                rem_cols.append(col)

    #Final fixes, if the user decides to remove a column, remove from everything
    final_data = tmp_df.drop(labels=rem_cols, axis=1)
    for key in rem_cols:
        del final_dict[key]
        del gmm_measures[key]

    return final_data, final_dict, gmm_measures
