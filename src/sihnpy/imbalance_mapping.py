""" Imbalance mapping module
"""

import pandas as pd
import numpy as np

def odregression_single(index, x, y):
    """ Function computing orthogonal regression. Was developped as an adaptation of the Pracma
    library in R. Results were tested against Pracma and scipy's ODR implementation.

    The ODR implementation uses Singular Value Decomposition (SVD) to find the model values. Note
    that `sihnpy`'s imbalance mapping really only requires the orthogonal distances from the models.
    As such, there isn't a lot of focus on the other model measures in this implementation.

    For more customization options, I recommend using SciPy's version which includes a lot more
    options: https://docs.scipy.org/doc/scipy/reference/odr.html#module-scipy.odr

    I'm far from a mathematician; I have adapted the code exactly, but I don't always fully
    understand what Pracma's developer did in some instances. As such, some steps are not always
    clear in terms of what they do. For more info, refer to Pracma's docs:
    https://rdrr.io/cran/pracma/man/odregress.html
    """

    #Prep objects we need
    variables_mat = np.column_stack((x, y)) #Concat independant and dependant variables
    n_indvar = np.shape(variables_mat)[1] - 1 #Grab number of independant variables

    #Create matrix of same shape as variables_mat, but each row is the average value of each column
    mean_mat = np.full((len(variables_mat), 2), np.mean(variables_mat, axis=0))

    #Execute singular value decomposition on the variables minus the mean
    # (i.e., right singular values when substracting the mean from the values).
    v_mat = np.linalg.svd(variables_mat - mean_mat)[2]

    #Compute intercept and slope of the regression. This is based on the right singular values from
    # the SVD.
    intercept = -v_mat[0:n_indvar, n_indvar] / v_mat[n_indvar, n_indvar]
    slope = np.mean(np.matmul(variables_mat, v_mat[n_indvar,:])) / v_mat[n_indvar, n_indvar]

    #Compute model measures (fit, residuals, orthogonal distances, sum of squares)
    fitted_values = np.matmul(
    ## Numpy will whine if not setting type to object.
        np.array([variables_mat[:,0], 1], dtype=object), 
        np.array([intercept, slope], dtype=object)
    )
    residuals = variables_mat[:,1] - fitted_values 

    normal = v_mat[:,n_indvar] #Not 100% sure what this does, but necessary to get the distances
    abs_orthogonal_distances = np.abs(np.matmul(variables_mat - mean_mat, normal)) #Orthogonal distances
    sig_orthogonal_distances = abs_orthogonal_distances*np.sign(residuals) #Same as above, but with the sign
    sum_square = sum(abs_orthogonal_distances**2) 

    #Store the values for export
    individual_values = pd.DataFrame(
        data={"participant_id":index,
            "y_values":variables_mat[:,n_indvar],
            "fitted_values":fitted_values,
            "residuals":residuals,
            "absolute_orthogonal_distances":abs_orthogonal_distances,
            "signed_orthogonal_distances":sig_orthogonal_distances}
    ).set_index('participant_id')

    model_fit = pd.DataFrame(
        data={"slope":slope, "intercept":intercept,"total_sum_of_squares":sum_square},
        index=['values']
    ).T #Flip the table so the metrics are the index instead of columns

    return individual_values, model_fit

def _pre_mapping(data):
    """ Computing variables needed for the imbalance mapping
    """

    num_regions = len(data.columns.values) #Compute number of brain regions
    num_participants = len(data) #Number of participants includes

    #Final array to hold the data per participant
    residual_array = np.empty((num_regions, num_regions, num_participants))

    return residual_array

def imbalance_mapping(data, type='sign'):
    """ Imbalance mapping function. For each column in the original data, compute covariance
    (i.e., regression) using orthogonal distance regression. Orthogonal distance is computed
    for each participant individually for each regression. We store the orthogonal distance
    for each participant, for each pair of brain region in a 3D symmetric matrix.

    The script gives the option of using either "absolute" or the "signed" distances. The sign
    add the distinction of showing whether a participant is below or above the regression line.
    """

    #Compute variables needed to run
    residual_array = _pre_mapping(data) #3D matrix. Axis 0 and 1 are the brain regions, 
    # axis 2 are participants

    #Loop over the data
    for i, region_i in enumerate(data):
        print(f'Computing region {i+1}/{len(data.columns)}')
        data_i = data[region_i]

        for j, region_j in enumerate(data):
            data_j = data[region_j]

            if type == 'abs':
                #Extract orthogonal distances from output of ODR
                odr_dist = odregression_single(index=data.index,
                        x=data_i.values, y=data_j.values)[0]['absolute_orthogonal_distances'].values
            else:
                odr_dist = odregression_single(index=data.index,
                        x=data_i.values, y=data_j.values)[0]['signed_orthogonal_distances'].values

            #Store the residuals in the 3D array.
            residual_array[i,j,:] = odr_dist #Order of the 3th dimension will match the input order

    return residual_array

def _by_person(residual_array):
    """ Imbalance Mapping creates a 3D matrix where the third dimension is the orthogonal distance
    for each participant. If we iterate over the 3rd dimension, we get the matrix refered to as C
    in Nadig's figure.
    """

    list_means = []

    for person in range(0, residual_array.shape[2]):
        #Extract person-wise array
        person_array = residual_array[:,:,person]

        #Extract upper triangle
        person_array_mod = person_array[np.triu_indices_from(person_array, k=1)]

        #Compute individuals' mean imbalance
        list_means.append(np.mean(person_array_mod))

    return list_means

def _by_region(residual_array):
    """ Imbalance Mapping creates a 3D matrix where the first and second
    dimension is the orthogonal distance for each region. The goal here
    is to create a sum on the 0 and 2 axis.
    """

    resid_copy = residual_array.copy()

    #Fill the diagonals of each person with missing values (as we don't want the correlation if i==j)
    for person in range(0, residual_array.shape[2]):
        np.fill_diagonal(resid_copy[:,:,person], np.NaN)

    return np.nanmean(resid_copy, axis=(0,2))

def _by_person_by_region(residual_array):
    """ Imbalance Mapping creates a 3D matrix where the first and second
    dimension is the orthogonal distance for each region. The goal here
    is to create a sum on the 0 axis. This will give, on
    average, how imbalanced each region is by person.
    """

    resid_copy = residual_array.copy()

    #Fill the diagonals of each person with missing values (as we don't want the correlation if i==j)
    for person in range(0, residual_array.shape[2]):
        np.fill_diagonal(resid_copy[:,:,person], np.NaN)  

    return np.nanmean(resid_copy, axis=0).T

def imbalance_stats(data, residual_array):
    """ Function computing the two measures from Nadig et al. (2021): we want the average imbalance
    by person and the average imbalance by region. Average imbalance by person is equivalent to taking
    the upper triangle of each of the matrix for each person and averaging all the data.

    Average imbalance by person is the equivalent of averaging each "horizontal slice" of the 3D
    matrix (i.e., averaging on the 0 and 2 dimension).
    """

    list_imbalance_person = _by_person(residual_array=residual_array)
    avg_by_region = _by_region(residual_array=residual_array)
    avg_imb_by_pers_by_region = _by_person_by_region(residual_array=residual_array)

    avg_imb_by_region = pd.DataFrame(index=data.columns.values, 
                                data=avg_by_region, columns=['avg_imbalance_by_region'])
    avg_imb_by_person = pd.DataFrame(index=data.index, 
                                data=list_imbalance_person, columns=['avg_imbalance_by_person'])

    avg_imb_by_pers_by_region = pd.DataFrame(index=data.index,
                                data=avg_imb_by_pers_by_region,
                                columns=data.columns.values)

    return avg_imb_by_region, avg_imb_by_person, avg_imb_by_pers_by_region

def export(data, residual_array, output_path, avg_imb_by_region, avg_imb_by_person, avg_imb_by_pers_by_region, name, all=False):
    """ Function to export the results of the imbalance mapping to files. If requested by the user
    `sihnpy` will also output the individual orthogonal distances matrices.
    """

    avg_imb_by_region.to_csv(f"{output_path}/avg_imbalance_by_region_{name}.csv")
    avg_imb_by_person.to_csv(f"{output_path}/avg_imbalance_by_person_{name}.csv")
    avg_imb_by_pers_by_region.to_csv(f"{output_path}/avg_imbalance_by_person_by_region_{name}.csv")

    if all is True: #Output all the individual imbalance mapping if user requests
        for i, person in enumerate(data.index.values):
            resid_i = residual_array[:,:,i]  #Extract individual matrix for each participant
            np.fill_diagonal(resid_i, np.NaN) #Fill the diagonal with missing values
            #Save the matrices
            np.savetxt(f"{output_path}/imbalance_{person}_{name}.txt", resid_i, fmt='%1.3f') 


