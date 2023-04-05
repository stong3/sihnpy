import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from scipy import stats
from matplotlib import pyplot as plt

# Spatial extent - Threshold derivation

def gmm_estimation(data_to_estimate, fix=False):
    """Function estimating a 1- and a 2-cluster solution Gaussian Mixture Model. The Bayesian
    Information Criteria is output and compared between the two models.

    Parameters
    ----------
    data_to_estimate : pandas.DataFrame
        Data where each column needs to be fed to the GMM. Any column where a GMM should NOT
        be estimated should have been removed
    fix : bool, optional
        Whether `sihnpy` should remove regions where 1-component fits better the data than a
        2-component model (using smallest Bayesian Information Criteria), by default False

    Returns
    -------
    dict, pandas.DataFrame
        Returns a dictionary with the GMM objects from `scikit-learn` and a `pandas.DataFrame`
        where columns were removed if fix is applied.
    """

    data = data_to_estimate.copy() #Copy the data to avoid modifying in place
    gm_estimations = {} #Dict to store GMM models
    col_rem_id = [] #List of columns to remove, if needed

    for col in data_to_estimate:
        print(f'GMM estimation for {col}')

        #For each column, sort the dataframe from lowest to highest and convert to 1D np.ndarray
        sorted_df = data.sort_values(by=col)
        roi_suvr = sorted_df[col].to_numpy().reshape(-1,1) #Need to reshape -1,1 since we feed 
                                                            #only 1 feature to the GMM

        #Estimate the GMM models (1 and 2 components)
        gm1 = GaussianMixture(n_components=1, random_state=667).fit(roi_suvr)
        gm2 = GaussianMixture(n_components=2, random_state=667).fit(roi_suvr)

        print(f"1-component: BIC = {gm1.bic(roi_suvr)} | 2-components: BIC = {gm2.bic(roi_suvr)} ")

        #Store GMM estimation object
        gm_estimations[col] = gm2

        #In the case that 1 distribution works better, here are the options
        if gm1.bic(roi_suvr) <= gm2.bic(roi_suvr):
            print("---GMM estimation suggests that 1 component is a better fit to the data")

            #If we want to remove the column with 1 component, save the ID here.
            if fix is True:
                print(f"----Fix is True: Region {col} will be removed from further calculation")
                col_rem_id.append(col)
                del gm_estimations[col]
            else:
                print(f"----Fix is False: Region {col} will be kept in the data")

    #Remove columns, if errors in estimation AND fix is true
    clean_data = data.drop(col_rem_id, axis=1)

    return gm_estimations, clean_data

def _gmm_avg_sd(gm_obj):
    """Quick function extracting and returning the average and SD values of the two components
    from the GMM estimation

    Parameters
    ----------
    gm_obj : sklearn.mixture.GaussianMixture
        Takes a GMM object as input

    Returns
    -------
    dict
        Returns a dictionary for each GMM object, with the mean and SDs of each component.
    """

    dict_gmm_measures = {}

    dict_gmm_measures[f'mean_comp1'] = gm_obj.means_[0][0]
    dict_gmm_measures[f'mean_comp2'] = gm_obj.means_[1][0]
    dict_gmm_measures[f'sd_comp1'] = np.sqrt(gm_obj.covariances_[0][0])[0]
    dict_gmm_measures[f'sd_comp2'] = np.sqrt(gm_obj.covariances_[1][0])[0]

    return dict_gmm_measures

def gmm_measures(cleaned_data, gm_objects, fix=False):
    """For all data kept after GMM estimation, this function computes the averages and SDs
    for both components.We then check that the order of the clusters is right and the 
    measures are also used for the histograms in the `spex.gmm_histograms` function.

    Parameters
    ----------
    cleaned_data : pandas.DataFrame
        Dataframe output from `spex.gmm_estimation`.
    gm_objects : dict
        Dictionary of the `sklearn.mixture.GaussianMixture` objects to extract measures from.
    fix : bool, optional
        If the mean of component 2 is lower than the mean of component 1, it suggests that the
        components are inverted. If fix is True, we remove the region from further calculations, 
        by default False

    Returns
    -------
    pandas.DataFrame, dict, dict
        Returns a Dataframe with clean data (if columns were removed by the fix), one dictionary
        with `sklearn.mixture.GaussianMixture` objects cleaned (if some estimations were removed)
        by fix and one dictionary with the averages/SDs of the two components, for regions kept.
    """

    tmp_df = cleaned_data.copy() #To avoid modifying the input.
    final_gm_estimations = gm_objects.copy() #To avoid modifying the input
    rem_cols = [] #For fixing if needed
    gmm_measures = {} #To store the GMM averages and SDs for histograms

    for col, gm_obj in final_gm_estimations.items():
        #Return averages and SDs of the components
        gmm_measures[col] = _gmm_avg_sd(gm_obj)

        #Check that average of second component is higher than the first component 
        if gmm_measures[col][f'mean_comp1'] > gmm_measures[col][f'mean_comp2']:
            print(f"Average of first component of {col} is higher than second component.")

            if fix is True:
                print(f'- Fix is true, removing {col}')
                rem_cols.append(col)

    #Final fixes, if the user decides to remove a column, remove from everything
    final_data = tmp_df.drop(labels=rem_cols, axis=1)
    for key in rem_cols: #For each region to remove
        del final_gm_estimations[key] #Remove from GMM estimation
        del gmm_measures[key] #Remove from GMM measures

    return final_data, final_gm_estimations, gmm_measures

def gmm_probs(final_data, final_gm_estimations, fix=False):
    """Function extracting the probability to be in the "second" component (high abnormal values).

    Parameters
    ----------
    final_data : pandas.DataFrame
        Cleaned dataframe output by `spex.gmm_measures`
    final_gm_estimations : dict
        Cleaned dictionary of `sklearn.mixture.GaussianMixture` objects output by 
        `spex.gmm_measures`
    fix : bool, optional
        If inverted distributions are not removed in `spex.gmm_measures`, they can be manually
        inverted here by setting to True, by default False

    Returns
    -------
    pandas.DataFrame
        Dataframe of the shape, index and columns from `final_data`. Contains probabilities of 
        belonging to the "abnormal" distribution for each participant, for each region.

    """

    probs_df = pd.DataFrame() #To store final data

    for col in final_data:
        sorted_df = final_data.sort_values(by=col) #Sort input index first so output matches
        probs = final_gm_estimations[col]\
            .predict_proba(sorted_df[col].to_numpy().reshape(-1,1)) #Find probability of each cluster from the GMM

        #Check whether components' means are inverted
        if final_gm_estimations[col].means_[1][0] < final_gm_estimations[col].means_[0][0]:
            print(f'-Means for components of {col} are inverted.')
            if fix is True:
                print(f'----Fix is True: Inverting the components...')
                tmp_df = pd.DataFrame(data=probs[:,0], 
                        index=sorted_df.index, columns=[col]) 
                #Extract and store the probability of cluster 1 when inversion issue.
            else:
                print(f'----Fix is False: Leaving as is.')
                tmp_df = pd.DataFrame(data=probs[:,1], 
                        index=sorted_df.index, columns=[col]) #Extract and store the probability of cluster 2
        else:
            #In any other case (no fixing, or fixing but components not inverted...)
            #Grab the probabilities of the second cluster
            tmp_df = pd.DataFrame(data=probs[:,1], 
                        index=sorted_df.index, columns=[col]) #Extract and store the probability of cluster 2

        probs_df = pd.concat([probs_df, tmp_df], axis=1) #Store probabilities for export

    return probs_df

def _gmm_density_histogram(regional_data, regional_gmm_measures, col, dist_2=True):
    """Histogram of the value DENSITIES with overlayed density function for each
    GMM cluster.

    Density is the count of each bin, divided by the total number of counts and the bin width.
    (Ref: Matplotlib documentation)
    This option is necessary to see the density curves.

    Parameters
    ----------
    regional_data : pandas.Series
        Single column from the `final_data` object representing the data in one region.
    regional_gmm_measures : dict
        Dictionary containing the mean and SD of each component.
    col : str
        String containing the name of the region. Used mostly for labels on the graphs.
    dist_2 : bool, optional
        Whether we want to plot one or two density functions (True == two), by default True

    Returns
    -------
    matplotlib.pyplot.figure
        Returns matplotlib figure
    """

    fig = plt.figure() #Instantiate figure
    plt.hist(regional_data, 50, density=True, facecolor='b', alpha=0.75) #Create histogram for the data
    plt.plot(np.sort(regional_data), stats.norm.pdf(np.sort(regional_data), 
                                                    regional_gmm_measures['mean_comp1'],
                                                    regional_gmm_measures['sd_comp1']),
            color='green', linewidth=4)  #Plots the density of component 1
    if dist_2 is True:
        plt.plot(np.sort(regional_data), stats.norm.pdf(np.sort(regional_data), 
                                                    regional_gmm_measures['mean_comp2'],
                                                    regional_gmm_measures['sd_comp2']),
            color='red', linewidth=4) #Plots the density of component 2
    plt.xlabel(f'Distribution of values {col}')
    plt.ylabel('Density of binned values')

    return fig

def _gmm_raw_histogram(regional_data, col):
    """Generates a simple histogram of the values in a given region. Can plot both the
    probabilities and the raw values, as needed.

    Parameters
    ----------
    regional_data : pandas.Series
        Single column of data for a single region (data or probabilities)
    col : str
        Name of the region of interest

    Returns
    -------
    matplotlib.pyplot.figure
        Returns matplotlib figure
    """

    fig = plt.figure() #Instantiate figure
    plt.hist(regional_data, 50, density=False, facecolor='b', alpha=0.75)
    plt.xlabel(f'Distribution of values {col}')
    plt.ylabel('Frequency of binned values')

    return fig

def gmm_histograms(final_data, gmm_measures, probs_df, dist_2=True, type="density"):
    """Optional function plotting histograms from the raw data, with overlayed density functions
    for both clusters.

    Parameters
    ----------
    final_data : pandas.DataFrame
        Dataframe from `spex.gmm_measures` with final columns to plot.
    gmm_measures : dict
        Nested dictionary containing the mean and SDs of each component, for each region.
    probs_df : pandas.DataFrame
        Dataframe of the probabilities of belonging to the "abnormal" distribution, from
        the `spex.gmm_probs` function.
    dist_2 : bool, optional
        Whether we want to plot one or two density functions (True == two) if we plot density,
        by default True
    type : str, optional
        Type of histogram to plot ("density", "raw", "probs", "all"), by default "density".

    Returns
    -------
    dict
        Returns a dictionary of matplotlib figures.
    """

    dict_fig = {}

    #For each region
    for col in final_data:
        if type == "density": #Density plot
            hist_dens = _gmm_density_histogram(final_data[col], gmm_measures[col], col=col,
                                                dist_2=dist_2)
            dict_fig[f'hist_density_{col}'] = hist_dens #Store in dictionary for export
            plt.close(hist_dens) #Close figure window to reduce memory usage

        elif type == "raw":
            hist_raw = _gmm_raw_histogram(final_data[col], col=col)
            dict_fig[f'hist_raw_{col}'] = hist_raw
            plt.close(hist_raw)

        elif type == "probs":
            hist_probs = _gmm_raw_histogram(probs_df[col], col=col)
            dict_fig[f'hist_probs_{col}'] = hist_probs
            plt.close(hist_probs)

        elif type == "all":
            hist_dens = _gmm_density_histogram(final_data[col], gmm_measures[col], 
                                                col=col, dist_2=dist_2)
            hist_raw = _gmm_raw_histogram(final_data[col], col=col)
            hist_probs = _gmm_raw_histogram(probs_df[col], col=col)

            dict_fig[f'hist_density_{col}'] = hist_dens
            dict_fig[f'hist_raw_{col}'] = hist_raw
            dict_fig[f'hist_probs_{col}'] = hist_probs

            plt.close(hist_dens)
            plt.close(hist_raw)
            plt.close(hist_probs)

    return dict_fig

def gmm_threshold_deriv(final_data, probs_df, prob_threshs, improb=None):
    """Function deriving the actual thresholds based on the probabilities of belonging to the
    "abnormal" distribution.

    Depending on the threshold value used, the probability of belonging to a given component
    can be inverted (e.g., the 50% probability threshold may have a higher value than the 90%
    threshold.). This usually happens when the second component is very spread out and overlaps
    with the first component. If that is the case, the use of the `improb` argument is recommended.

    Also note that to give more flexibility to the user, `sihnpy` allows for a list of thresholds
    to be given to derive multiple thresholds. However, `sihnpy` doesn't check whether the order
    of the thresholds make sense (e.g., that 50% comes before 90%) and assumes the user put them
    in the right order. It is up to the user to check this once the thresholds are derived.

    Parameters
    ----------
    final_data : pandas.DataFrame
        Final data derived from `spex.gmm_measures`. 
    probs_df : pandas.DataFrame
        Dataframe containing the probabilities of belonging to the "abnormal" distribution, from
        the `spex.gmm_probs` function.
    prob_threshs : list of float
        List of thresholds to apply to the data. Thresholds have to range between 0 and 1.
    improb : float, optional
        Value below which an "abnormal" value is improbable or impossible. Useful in the case that
        the GMM is very spread out, by default None

    Returns
    -------
    pandas.DataFrame
        Dataframe where rows are the regions and columns are the thresholds derived from the probabilities.
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
                    i = 0
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
                        #In case no values go over the improbable threshold after a few tries,
                        # we forcibly set that threshold to missing.
                        else:
                            i += 1
                            if i == 10:
                                print(f"---Can't fix thresholds for {col}. Setting to missing.")
                                thresh_df.loc[col, f'thresh_{thresh}'] = np.NaN
                                fix = True
                else:
                    #If the value is not improbable, simply save it
                    thresh_df.loc[col, f'thresh_{thresh}'] = thresh_value
            else:
                #If the correction is turned off, we simply save the value regardless
                thresh_df.loc[col, f'thresh_{thresh}'] = thresh_value

    return thresh_df

def export_histograms(hist_dict_fig, output_path, name):
    """ Exporting the histograms to file, if requested by user. Will export ALL
    histograms saved to the dictionary    

    Parameters
    ----------
    hist_dict_fig : dict
        Dictionary of histogram figures from `spex.gmm_histograms`
    output_path : str
        String of the path to where the output should go
    name : str
        Name that should be tacked at the end of the file name, depending on the user's 
        conventions.
    """

    for type_hist, hist in hist_dict_fig.items():
        hist.savefig(f'{output_path}/{type_hist}_{name}.png', dpi=500)

def export_threshs(final_data, probs_data, thresh_df, output_path, name):
    """ Wrapper function exporting the final data used and the probability data to files.

    Parameters
    ----------
    final_data : pandas.DataFrame
        Final data derived from `spex.gmm_measures`. 
    probs_df : pandas.DataFrame
        Dataframe containing the probabilities of belonging to the "abnormal" distribution, from
        the `spex.gmm_probs` function.
    thresh_df : pandas.DataFrame
        Dataframe containing the thresholds we just derived
    output_path : str
        String of the path to where the output should go
    name : str
        Name that should be tacked at the end of the file name, depending on the user's 
        conventions.
    """
    final_data.to_csv(f"{output_path}/final_data_derived_{name}.csv")
    probs_data.to_csv(f"{output_path}/probabilities_clust2_{name}.csv")
    thresh_df.to_csv(f"{output_path}/thresholds_{name}.csv")

# Spatial extent - Threshold application
def apply_clean(data_to_apply, thresh_data, index_name=None):
    """Function doing basic cleaning on the spatial extent and thresholds; just sorts
    the rows and make sure they match between the thresholds and data to apply.

    Parameters
    ----------
    data_to_apply : pandas.DataFrame
        Data on which we want to apply thresholds. Columns should match rows of `thresh_data`.
    thresh_data : pandas.DataFrame
        Thresholds to be applied to the data. Rows should match columns of `data_to_apply`.
    index_name : str, optional
        String indicating the name of the column that should be considered as the 
        `pandas.DataFrame.Index`. By default, assume it's already set; by default None

    Returns
    -------
    pandas.DataFrame
        Returns `pandas.DataFrame` of the data, where the columns of the data shares the same
        order as the rows of the thresholds.
    """

    #If the index name is given by the user, we set the index first or it will be discarded later.
    if index_name is not None:
        #Set index, keep columns that match the index of the threshold file and sort columns
        data_to_apply_clean = data_to_apply\
            .set_index(index_name)\
            .filter(items=thresh_data.index, axis=1)\
            .sort_index(axis=1)
    else:
        data_to_apply_clean = data_to_apply\
            .filter(items=thresh_data.index, axis=1)\
            .sort_index(axis=1)

    #Filter rows to keep only those that appear in the columns of the data and sort the index
    thresh_data_clean = thresh_data\
        .filter(items=data_to_apply_clean.columns, axis=0)\
        .sort_index(axis=0)

    if len(thresh_data_clean) != len(data_to_apply_clean.columns):
        return f"Error: Rows in the threshold data ({len(thresh_data_clean)}) doesn't equal to the columns in the data to apply ({len(data_to_apply.columns)})"

    return data_to_apply_clean, thresh_data_clean

def apply_masks(data_to_apply_clean, thresh_data_clean):
    """Function applying the thresholds to the data, resulting in binary masks. The binary masks
    have the same shape as the original data (rows are participants, columns are regions). The
    number of masks depends on the number of thresholds (columns) in `thresh_data_clean`.

    Parameters
    ----------
    data_to_apply_clean : pandas.DataFrame
        Data to which we want to apply the spatial extent, where columns are regions and rows
        are participants. From `spex.apply_clean`.
    thresh_data_clean : pandas.DataFrame
        Dataframe containing the threshold data, where rows are regions and columns are thresholds.
        From `spex.apply_clean`

    Returns
    -------
    dict
        Returns a dictionary of `pandas.DataFrame`s, where each `DataFrame` contains binary values
        for each region, for each participant.
    """

    dict_masks = {}

    #For each threshold value...
    for threshold in thresh_data_clean:
        #Create an empty DF to store all the regional binary values
        tmp_df = pd.DataFrame(index=data_to_apply_clean.index)

        #For each region in the DF we want to apply the thresholds to
        for region in data_to_apply_clean:
            #If the region has a threshold available
            if region in thresh_data_clean.index:
                #Apply the threshold, where 1 is above or equal to threshold
                tmp_df[region] = np.where(data_to_apply_clean[region]
                                >= thresh_data_clean.loc[region, threshold], 1, 0)

        #Store the data in a dictionary, classified by thresholds
        dict_masks[f'{threshold}'] = tmp_df

    return dict_masks

def apply_index(data_to_apply_clean, dict_masks):
    """Create the spatial extent index, which is the sum of regions that are above the threshold.
    In the case where multiple thresholds are available we output the sum of each thresholds 
    individually, as well as the total sum of all thresholds together.

    Parameters
    ----------
    data_to_apply_clean : pandas.DataFrame
        Original dataframe cleaned with `spex.apply_clean`. Only used to get the index to
        ensure the spatial extent is the same order.
    dict_masks : dict
        Dictionary containing all the binary masks from `spex.apply_masks`

    Returns
    -------
    pandas.DataFrame
        Dataframe containing the spatial extent index for each threshold.
    """

    #Create empty dataframe with the same index as the original data
    spex_metrics = pd.DataFrame(index=data_to_apply_clean.index)

    #Compute the spatial extent, by summing rows (i.e., within each participant)
    for threshold_val, masks in dict_masks.items():
        spex_metrics[f'spatial_extent_{threshold_val}'] = masks.sum(axis=1) #Sum the rows to get spatial extent index

    #If more than 1 threshold, we also compute a sum of regions for all thresholds
    if len(spex_metrics.columns) > 1:
        spex_metrics[f'spatial_extent_sum_all'] = spex_metrics.sum(axis=1)

    return spex_metrics

def apply_ind_mask(data_to_apply_clean, dict_masks):
    """Another way to leverage the spatial extent is by creating individualized spatial extent
    masks. The idea is that simply add weights to the original data, based on the probability of
    being abnormal in a given region.

    For instance, if a participant has a 90% probability of being positive, vs a 50% probability
    of being positive, we give more weight to the 90% probability value by multiplying it by
    a different constant.

    Parameters
    ----------
    data_to_apply_clean : pandas.DataFrame
        Original dataframe cleaned with `spex.apply_clean`.
    dict_masks : dict
        Dictionary containing all the binary masks from `spex.apply_masks`

    Returns
    -------
    dict
        Dictionary of individualized spatial extent masks.
    """

    spex_ind_masks = {}
    dict_masks_copy = dict_masks.copy()
    tmp_data = pd.DataFrame()

    #If more than one mask, create a sum of masks
    if len(dict_masks) > 1:
        for masks in dict_masks.values():
            tmp_data = tmp_data.add(masks, fill_value=0) 
            #If original value was missing, the result will be missing. We force 0 to be everywhere

        #Store that new mask in the dictionary for output
        dict_masks_copy['mask_spatial_extent_sum_all'] = tmp_data

    #For each mask, compute the individualized mask
    for threshold_vals, masks in dict_masks_copy.items():
        spex_ind_masks[threshold_vals] = data_to_apply_clean.multiply(masks)\
            .replace(to_replace={0:np.NaN})

    return spex_ind_masks

def export_spex_metrics(spex_metrics, output_path, name):
    """Function to export the spatial extent metrics.

    Parameters
    ----------
    spex_metrics : pandas.DataFrame
        Dataframe containing the spatial extent indices.
    output_path : str
        Path where the dataframe should be output.
    name : str
        String that should be tacked at the end of the file name based on user convention.
    """

    spex_metrics.to_csv(f"{output_path}/spex_metrics_{name}.csv")

def export_spex_bin_masks(dict_masks, output_path, name):
    """Function to export the binary masks.

    Parameters
    ----------
    dict_masks : dict
        Dictionary of binary masks where the thresholds were applied.
    output_path : str
        Path where the dataframe should be output.
    name : str
        String that should be tacked at the end of the file name based on user convention.
    """
    for name_mask, masks in dict_masks.items():
        masks.to_csv(f"{output_path}/spex_bin_mask_{name_mask}_{name}.csv")

def export_spex_ind_masks(spex_ind_masks, output_path, name):
    """Function to export the individualized spatial extent masks

    Parameters
    ----------
    spex_ind_masks : dict
        Dictionary of individualized spatial extent masks
    output_path : str
        Path where the dataframe should be output.
    name : str
        String that should be tacked at the end of the file name based on user convention.
    """
    for name_mask, masks in spex_ind_masks.items():
        masks.to_csv(f"{output_path}/spex_ind_mask_{name_mask}_{name}.csv")

