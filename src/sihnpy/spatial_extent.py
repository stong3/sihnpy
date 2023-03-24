import os
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from scipy import stats
from matplotlib import pyplot as plt

# Spatial extent - Threshold derivation

def gmm_estimation(data_to_estimate, fix=False):
    """ Function estimating a 1- and a 2-cluster solution Gaussian Mixture Model. The Bayesian
    Information Criteria is output and compared between the two models.
    """

    data = data_to_estimate.copy()
    gm_estimations = {}
    col_rem_id = []

    for col in data_to_estimate:
        print(f'GMM estimation for {col}')

        #For each column, sort the dataframe from lowest to highest and convert to 1D np.ndarray
        sorted_df = data.sort_values(by=col)
        roi_suvr = sorted_df[col].to_numpy().reshape(-1,1)

        #Estimate the GMM models
        gm1 = GaussianMixture(n_components=1, random_state=667).fit(roi_suvr)
        gm2 = GaussianMixture(n_components=2, random_state=667).fit(roi_suvr)

        print(f"1-component: BIC = {gm1.bic(roi_suvr)} | 2-components: BIC = {gm2.bic(roi_suvr)} ")

        #Store GMM estimation object
        gm_estimations[col] = gm2

        #In the case that 1 distribution works better, here are the options
        if gm1.bic(roi_suvr) <= gm2.bic(roi_suvr):
            print("GMM estimation suggests that 1 component is a better fit to the data")

            #If we want to remove the column with 1 component, save the ID here.
            if fix is True:
                print(f"-Fix is True: Region {col} will be removed from further calculation")
                col_rem_id.append(col)
                del gm_estimations[col]
            else:
                print(f"-Fix is False: Region {col} will be kept in the data")

    #Remove columns, if errors in estimation AND fix is true
    clean_data = data.drop(col_rem_id, axis=1)

    return gm_estimations, clean_data

def _gmm_avg_sd(gm_obj):
    """ Quick function extracting and returning the average and SD values of the two components.
    """
    dict_gmm_measures = {}

    dict_gmm_measures[f'mean_comp1'] = gm_obj.means_[0][0]
    dict_gmm_measures[f'mean_comp2'] = gm_obj.means_[1][0]
    dict_gmm_measures[f'sd_comp1'] = np.sqrt(gm_obj.covariances_[0][0])[0]
    dict_gmm_measures[f'sd_comp2'] = np.sqrt(gm_obj.covariances_[1][0])[0]

    return dict_gmm_measures

def gmm_measures(cleaned_data, gm_objects, fix=False):
    """ For all data kept after GMM estimation, compute the averages and SDs for both components.
    We then check that the order of the clusters is right and the measures are also used for
    the histograms.

    Finally, we compute the probabilities of belonging to the second cluster for each region. We
    will save that probability for the threshold determination.
    """

    tmp_df = cleaned_data.copy() #To avoid modifying the input.
    final_gm_dict = gm_objects.copy() #To avoid modifying the input
    rem_cols = [] #For fixing if needed
    gmm_measures = {} #To store the GMM averages and SDs for histograms

    for col, gm_obj in final_gm_dict.items():
        #Return averages and SDs of the components
        gmm_measures[col] = _gmm_avg_sd(gm_obj)

        #Check that average of second component is higher than the first component 
        if gmm_measures[col][f'mean_comp1'] > gmm_measures[col][f'mean_comp2']:
            print(f"Average of first component of {col} is higher than second component.")

            if fix is True:
                rem_cols.append(col)

    #Final fixes, if the user decides to remove a column, remove from everything
    final_data = tmp_df.drop(labels=rem_cols, axis=1)
    for key in rem_cols:
        del final_gm_dict[key]
        del gmm_measures[key]

    return final_data, final_gm_dict, gmm_measures

def gmm_probs(final_data, final_gm_dict, fix=False):
    """ Function extracting the probability to be in the "second" distribution (high abnormal values)
    """

    probs_df = pd.DataFrame()

    for col in final_data:
        sorted_df = final_data.sort_values(by=col) #Sort input index first so output matches
        probs = final_gm_dict[col]\
            .predict_proba(sorted_df[col].to_numpy().reshape(-1,1)) #Find probability of each cluster from the GMM

        if final_gm_dict[col].means_[1][0] < final_gm_dict[col].means_[0][0]:
            print(f'Means for components of {col} are inverted.')
            if fix is True:
                print(f'Inverting the components...')
                tmp_df = pd.DataFrame(data=probs[:,0], 
                        index=sorted_df.index, columns=[col]) 
                #Extract and store the probability of cluster 1 when inversion issue.
        else:
            #In any other case (no fixing, or fixing but components not inverted...)
            #Grab the probabilities of the second cluster
            tmp_df = pd.DataFrame(data=probs[:,1], 
                        index=sorted_df.index, columns=[col]) #Extract and store the probability of cluster 2

        probs_df = pd.concat([probs_df, tmp_df], axis=1) #Store probabilities for export

    return probs_df

def _gmm_density_histogram(regional_data, regional_gmm_measures, col, dist_2=True):
    """ Histogram of the value DENSITIES () with overlayed density function for each
    GMM cluster.

    Density is the count of each bin, divided by the total number of counts and the bin width.
    This option is necessary to see the density curves.
    """

    fig = plt.figure() #Instantiate figure
    plt.hist(regional_data, 50, density=True, facecolor='b', alpha=0.75) #Create histogram for the data
    plt.plot(np.sort(regional_data), stats.norm.pdf(np.sort(regional_data), 
                                                    regional_gmm_measures['mean_comp1'],
                                                    regional_gmm_measures['sd_comp1']),
            color='green', linewidth=4) 
    if dist_2 is True:
        plt.plot(np.sort(regional_data), stats.norm.pdf(np.sort(regional_data), 
                                                    regional_gmm_measures['mean_comp2'],
                                                    regional_gmm_measures['sd_comp2']),
            color='red', linewidth=4) 
    plt.xlabel(f'Distribution of values {col}')
    plt.ylabel('Density of binned values')

    return fig

def _gmm_raw_histogram(regional_data, col):
    """ Generates a simple histogram of the values in a given region. Can plot both the
    probabilities and the raw values, as needed.
    """

    fig = plt.figure() #Instantiate figure
    plt.hist(regional_data, 50, density=False, facecolor='b', alpha=0.75)
    plt.xlabel(f'Distribution of values {col}')
    plt.ylabel('Frequency of binned values')

    return fig

def gmm_histograms(final_data, gmm_measures, probs_df, dist_2=True, type="density"):
    """Optional function plotting histograms from the raw data, with overlayed density functions
    for both clusters.
    """

    dict_fig = {}

    for col in final_data:
        if type == "density":
            hist_dens = _gmm_density_histogram(final_data[col], gmm_measures[col], col=col,
                                                dist_2=dist_2)
            dict_fig[f'hist_density_{col}'] = hist_dens

        elif type == "raw":
            hist_raw = _gmm_raw_histogram(final_data[col], col=col)
            dict_fig[f'hist_raw_{col}'] = hist_raw

        elif type == "probs":
            hist_probs = _gmm_raw_histogram(probs_df[col], col=col)
            dict_fig[f'hist_probs_{col}'] = hist_probs

        elif type == "all":
            hist_dens = _gmm_density_histogram(final_data[col], gmm_measures[col], 
                                                col=col, dist_2=dist_2)
            hist_raw = _gmm_raw_histogram(final_data[col], col=col)
            hist_probs = _gmm_raw_histogram(probs_df[col], col=col)

            dict_fig[f'hist_density_{col}'] = hist_dens
            dict_fig[f'hist_raw_{col}'] = hist_raw
            dict_fig[f'hist_probs_{col}'] = hist_probs

    return dict_fig

def gmm_threshold_deriv(final_data, probs_df, prob_threshs, improb):
    """ Function deriving the actual thresholds based on the probabilities of belonging to the high values group.

    NOTE: Depending on the threshold value used, the probability of belonging to a given cluster
    can be inverted (e.g., the 50% probability threshold may have a higher value than the 90%
    threshold.). If there are no issues of 1 vs 2 distributions and the clusters are in the right
    order, normally there is no issue at this step.

    To give more flexibility to the user, SIHNpy allows for a list of thresholds to be given, but
    it doesn't check whether the order makes sense. It is up to the user to check this once the
    thresholds are derived.
    """

    if not isinstance(prob_threshs, list):
        return "Error: The threshold derivation is expecting a list of values, even if only 1 threshold is given."

    #Create empty dataframe to store all the thresholds
    thresh_df = pd.DataFrame(index=final_data.columns.values, data=None)

    #Sort the thresholds to get the lowest to the highest probability.
    prob_threshs.sort()

    #For each threshold...
    for thresh in prob_threshs:
        #For each region...
        for col in final_data:

            #Sort the indices of the raw values and probabilities to make sure they match
            raw_sorted = final_data[col].sort_index(level=0)
            probs_sorted = probs_df[col].sort_index(level=0)

            #Quick check that the raw values and probabilities have the same index 
                # (i.e., number of participants)
            if raw_sorted.index.equals(probs_sorted.index) is False:
                return "Error: The raw data and probability data don't share the same index."

            #Find the closest probability to the probability threshold
            id_prob_min = (np.abs(probs_sorted - thresh)).argmin()

            #Find the raw value of the participant with closest probability to the threshold
            thresh_value = raw_sorted.iloc[id_prob_min]

            #In some cases, the probability assigned by the GMM causes the thresholds
            # to be dramatically low. We can fix it by forcing values that would
            # be improbable and ignoring values that are improbable when creating
            # the threshold. This step is optional
            if improb is not None: 
                #If the threshold is below the biologically plausible value
                if thresh_value < improb:
                    print(f"Threshold for {col} is improbable. Fixing.")
                    fix = False
                    #While the value is improbable, keep trying to find a value
                    while fix is False:
                        #Set the old probability to 0 to ignore it
                        probs_sorted.iloc[id_prob_min] = 0
                        #Recompute the closest probability and find threshold
                        id_prob_min = (np.abs(probs_sorted - thresh)).argmin()
                        thresh_value = raw_sorted.iloc[id_prob_min]

                        #If the value is higher than the improbable value, we are done
                        if thresh_value > improb:
                            #Save the new value and switch the loop off
                            thresh_df.loc[col, f'thresh_{thresh}'] = thresh_value
                            fix = True
                else:
                    #If the value is not improbable, simply save it
                    thresh_df.loc[col, f'thresh_{thresh}'] = thresh_value
            else:
                #If the correction is turned off, we simply save the value regardless
                thresh_df.loc[col, f'thresh_{thresh}'] = thresh_value

    return thresh_df

def export_histograms(hist_dict_fig, output_path, name):
    """ Exporting the histograms to file, if requested by user
    """

    for type_hist, hist in hist_dict_fig.items():
        hist.savefig(f'{output_path}/{type_hist}_{name}.png', dpi=500)

def export_thresholds(thresh_df, output_path, name):
    """ Exporting thresholds to file, if requested by user
    """

    thresh_df.to_csv(f"{output_path}/thresholds_{name}.csv")

def export_probs_suvrs(final_data, probs_data, output_path, name):
    """ Quick function exporting the final data used and the probability data
    """
    final_data.to_csv(f"{output_path}/final_data_derived_{output_path}_{name}.csv")
    probs_data.to_csv(f"{output_path}/probabilities_clust2_{output_path}_{name}.csv")

# Spatial extent - Threshold application
def apply_clean(data_to_apply, index_name, thresh_data):
    """ Function doing basic cleaning on the spatial extent and thresholds. Basically just sorts
    the rows and make sure they match between the thresholds and data to apply.
    """

    data_to_apply_clean = data_to_apply\
        .set_index(index_name)\
        .filter(items=thresh_data.index, axis=1)\
        .sort_index(axis=1)

    thresh_data_clean = thresh_data\
        .sort_index(axis=0)

    return data_to_apply_clean, thresh_data_clean

def apply_masks(data_to_apply_clean, thresh_data_clean):
    """ Function applying the thresholds to the data, resulting in binary masks.
    """

    dict_masks = {}

    #For each threshold value...
    for threshold in thresh_data_clean:
        #Create an empty DF to store all the regional binary values
        tmp_df = pd.DataFrame(index=data_to_apply_clean.index)

        #For each region in the DF we want to apply the thresholds to
        for region in data_to_apply_clean:
            #If the region has a threshold available
            if region in data_to_apply_clean.index:
                #Apply the threshold, where 1 is above or equal to threshold
                tmp_df[region] = np.where(data_to_apply_clean[region]
                                >= thresh_data_clean.loc[region, threshold], 1, 0)

        #Store the data in a dictionary, classified by thresholds
        dict_masks[f'{threshold}'] = tmp_df

    return dict_masks

def apply_index(data_to_apply_clean, dict_masks):
    """Create the spatial extent index, which is the sum of regions that are above the threshold.
    In the case where multiple thresholds are available we output the sum of each thresholds individually, as well as the total sum of all thresholds together.
    """

    spex_metrics = pd.DataFrame(index=data_to_apply_clean.index)

    for threshold_val, masks in dict_masks.items():
        spex_metrics[f'spatial_extent_{threshold_val}'] = masks.sum(axis=1) #Sum the rows to get spatial extent index

    if len(spex_metrics) > 1:
        spex_metrics[f'spatial_extent_sum_all'] = spex_metrics.sum(axis=1)

    return spex_metrics

def apply_ind_mask(data_to_apply_clean, dict_masks):
    """ Another way to leverage the spatial extent is by creating individualized spatial extent
    masks. The idea is that simply add weights to the original data, based on the probability of
    being abnormal in a given region.

    For instance, if a participant has a 90% probability of being positive, vs a 50% probability
    of being positive, we give more weight to the 90% probability value by multiplying it by
    a different constant.
    """

    spex_ind_masks = {}

    for threshold_vals, masks in dict_masks.items():
        spex_ind_masks[threshold_vals] = data_to_apply_clean.multiply(masks)\
            .replace(to_replace={0:np.NaN})

    return spex_ind_masks

def export_spex_metrics(spex_metrics, output_path, name):
    """ Function to export the spatial extent metrics we calculated.
    """
    spex_metrics.to_csv(f"{output_path}/spex_metrics_{name}.csv")

def export_spex_ind_masks(spex_ind_masks, output_path, name):
    """ Function to export the spatial extent individual masks.
    """
    for name_mask, masks in spex_ind_masks.items():
        masks.to_csv(f"{output_path}/spex_ind_mask_{name_mask}_{name}.csv")

