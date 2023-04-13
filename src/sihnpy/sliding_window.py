import os
import math

import pandas as pd
import numpy as np

# Sliding-window

def bins(data, var, w_size, s_size, collapse=False):
    """ Sliding-window function estimating the number of bins to compute.

    Future options: allow for missing values (choose to sort them and put them first or last, or just remove them).
    """

    #Check missing values. If missing, we can't compute.
    if data[var].isnull().values.any():
        return f"Couldn't compute number of bins: there are missing values in '{var}'"
    
    #Sort the variable of interest.
    sorted_df = data.sort_values(by=var, axis=0, ascending=True)

    #Compute number of participants
    n_sub = len(sorted_df)

    #Compute the bins
    ## First situation: dividing with window params yields clean division
    if collapse is True:
        print("Collapse is True: the last window may have a larger number of participants")
        n_bin = math.ceil((n_sub - w_size) / s_size)
        print(f'Number of windows: {n_bin}')
    ##Second situation: dividing the window params doesn't yield a clean division.
    ## in that case, there are more participants, but not enough to make a full other window.
    else:
        print("Collapse is False: the last window may have a smaller number of participants")
        n_bin = math.ceil((n_sub - w_size) / s_size) + 1
        print(f'Number of windows: {n_bin}')

    return n_bin

def build_windows(data, var, w_size, s_size, n_bin):
    """ Function deriving the participants in each window. Returns a pandas.DataFrame with only an
    index. 

    Note: In the original script, the code creating "bin_list" has an extra +1. This was because R
    is 1-indexed. However, Python is 0-indexed, so it needs to start at 0.

    """

    w_store = {} #Store the windows once computed

    #Check missing values. If missing, we can't compute.
    if data[var].isnull().values.any():
        return f"Couldn't compute number of bins: there are missing values in '{var}'"
    
    #Sort the variable of interest, keep only the sorting variable
    sorted_df = data.sort_values(by=var, axis=0, ascending=True)\
        .filter(items=[var], axis=1)

    #Grab the participants for each window
    for bin in range(0, n_bin):
        bin_id = bin + 1 #Create an ID for each bin. Mostly to match the original R code.
        #Mostly makes the printing a bit more readable since it's not 0-indexed
        print(f"Creating bin {bin_id}")

        if bin_id == n_bin: #If we reach the last window...
            bin_list = sorted_df.iloc[(s_size * (bin_id - 1)):] #... grab all remainding participants
        else: #For every window except the last
            bin_list = sorted_df.iloc[(s_size * (bin_id - 1)):
                                      (w_size + s_size * (bin_id - 1))] 
            #Grab from the start of the step size to the end of the new window

        #Create the name of the bin, to be used for saving the files
        if bin + 1 >= 10:
            bin_name = f"ww{w_size}_sts{s_size}_w{bin + 1}"
        else:
            bin_name = f"ww{w_size}_sts{s_size}_w0{bin + 1}"

        #Store the list of participants
        w_store[f'{bin_name}'] = bin_list.filter(items=[]) #Keeping only the index

    return w_store

def data_by_window(w_store, data):
    """ This function separates the data in age windows.
    """

    w_data = {} #Dict to store the data in windows

    for labels, win_ids in w_store.items():
        #Merge the data to the index we extracted
        merged_data = win_ids.merge(data, left_index=True, right_index=True, how='left')
        w_data[labels] = merged_data #Save the dataframe

    return w_data

def sum_by_window(w_data, var):
    """ This function outputs summary measures for the
    binning variable for each window.
    """

    w_summary = pd.DataFrame() #Dataframe to store the summary measures

    #Compute the summary measures for each window
    for labels, win_data in w_data.items():
        mean_var = win_data[var].mean()
        median_var = win_data[var].median()
        sd_var = win_data[var].std()
        min_var = win_data[var].min()
        max_var = win_data[var].max()

        #Store in df
        tmp_df = pd.DataFrame(data={'window':[labels], 
                                    f"mean_{var}": mean_var,
                                    f"median_{var}":median_var,
                                    f"sd_{var}":sd_var,
                                    f"min_{var}":min_var,
                                    f"max_{var}":max_var})

        #Save to dataframe
        w_summary = pd.concat([w_summary, tmp_df], ignore_index=True) 

    return w_summary.set_index('window')

def export_data(w_data, w_summary, var, path, name):
    """ Function exporting sliding window information.
    """

    #Save data for individual windows
    for labels, data in w_data.items():

        #Save full data for each window
        data.to_csv(f'{path}/full_data_{labels}_{name}.csv')

        #Save IDs for each window
        np.savetxt(f'{path}/ids_{labels}_{name}.txt', data.index.values, newline=os.linesep, fmt='%s') #

    #Save the summaries by window
    w_summary.to_csv(f'{path}/summary_{var}_by_window_{name}.csv')