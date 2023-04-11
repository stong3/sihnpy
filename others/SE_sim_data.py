""" Script generating simulated data for spatial extent project

Quick script generating simulated data to test the spatial extent module functionalities.
We want to create about 10 brain regions from Gaussian noise. We also want 2 regions
to showcase issues that can arise from spatial extent.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.mixture import GaussianMixture
from matplotlib import pyplot as plt

def gen_random_population(mean1, sd1, size1, mean2, sd2, size2):
    """Generates random data mimicking tau-PET SUVR data, of the size of the PREVENT-AD Open
    dataset, by pulling 308 sample data points from 2 randomly generated populations.

    Parameters
    ----------
    mean1 : float
        Mean of the first distribution
    sd1 : float
        Standard deviation of the first distribution
    size1 : int
        Size of the first population
    mean2 : float
        Mean of the second distribution
    sd2 : float
        Standard deviation of the second distribution
    size2 : int
        Size of the second population

    Returns
    -------
    numpy.array
        Numpy array containing the 308 random data points; 100 AD, 208 CU
    """
    np.random.seed(667)
    #Create a random population based on CU and on AD. Concatenate
    pop_sim_neg_data = np.random.choice(stats.norm.rvs(mean1, sd1, size1, random_state=667), 208)
    pop_sim_pos_data = np.random.choice(stats.norm.rvs(mean2, sd2, size2, random_state=667), 100)

    return np.concatenate((pop_sim_neg_data, pop_sim_pos_data))

def gmm_calculation(data):
    """ Function computing a single- and two-components GMM
    """

    gm1 = GaussianMixture(n_components=1, random_state=667).fit(np.sort(data).reshape(-1,1))
    gm2 = GaussianMixture(n_components=2, random_state=667).fit(np.sort(data).reshape(-1,1))

    bic1 = gm1.bic(data.reshape(-1,1))
    bic2 = gm2.bic(data.reshape(-1,1))

    return gm1, gm2, bic1, bic2

def gmm_distribution_metrics(gm, dist_2 = False):
    """ Simple function computing the mean and standard deviation of the two distribution
    from the GMM calculations. These measures will be used for plotting purposes
    """

    dict_gm = {}

    dict_gm['mean_dist_1'] = gm.means_[0][0]
    dict_gm['sd_dist_1'] = np.sqrt(gm.covariances_[0][0])[0]

    if dist_2 is True:
        dict_gm['mean_dist_2'] = gm.means_[1][0]
        dict_gm['sd_dist_2'] = np.sqrt(gm.covariances_[1][0])[0]

    return dict_gm

def gmm_plot_distributions(data, dict_gm, name, dist_2 = False):
    """ Function plotting the data for the distribution and overlays the density function
    from the two distribution (if applicable)
    """
    fig = plt.figure() #Instantiate figure
    plt.hist(data, 50, density=True, facecolor='b', alpha=0.75) #Create histogram for the data
    plt.plot(np.sort(data), stats.norm.pdf(np.sort(data), dict_gm['mean_dist_1'], dict_gm['sd_dist_1']), 
        color='green', linewidth=4) #Plot density of first distribution / Sort data otherwise will cause an alien plot to appear
    if dist_2 is True:
        plt.plot(np.sort(data), stats.norm.pdf(np.sort(data), dict_gm['mean_dist_2'], dict_gm['sd_dist_2']),
            color='red', linewidth=4) #Plot density of second distribution, if needed
    plt.xlabel(f'Distribution SUVR values {name} region')
    plt.ylabel('Frequency of SUVR values (bins)')

    return fig

dict_random_tau_data = {}

dict_random_tau_data["CTX_LH_ENTORHINAL_SUVR"] = gen_random_population(mean1=1.119, sd1=0.110, size1=10000, mean2=1.578, sd2=0.321, size2=10000)
dict_random_tau_data["CTX_RH_ENTORHINAL_SUVR"] = gen_random_population(mean1=1.122, sd1=0.099, size1=10000, mean2=1.582, sd2=0.300, size2=10000)
dict_random_tau_data["CTX_LH_AMYGDALA_SUVR"] = gen_random_population(mean1=1.125, sd1=0.112, size1=10000, mean2=1.642, sd2=0.299, size2=10000)
dict_random_tau_data["CTX_RH_AMYGDALA_SUVR"] = gen_random_population(mean1=1.127, sd1=0.107, size1=10000, mean2=1.632, sd2=0.272, size2=10000)
dict_random_tau_data["CTX_LH_FUSIFORM_SUVR"] = gen_random_population(mean1=1.185, sd1=0.112, size1=10000, mean2=1.690, sd2=0.506, size2=10000)
dict_random_tau_data["CTX_RH_FUSIFORM_SUVR"] = gen_random_population(mean1=1.175, sd1=0.078, size1=10000, mean2=1.665, sd2=0.485, size2=10000)
dict_random_tau_data["CTX_LH_PARAHIPPOCAMPAL_SUVR"] = gen_random_population(mean1=1.097, sd1=0.095, size1=10000, mean2=1.450, sd2=0.292, size2=10000)
dict_random_tau_data["CTX_RH_PARAHIPPOCAMPAL_SUVR"] = gen_random_population(mean1=1.091, sd1=0.079, size1=10000, mean2=1.442, sd2=0.313, size2=10000)
dict_random_tau_data["CTX_LH_INFERIORTEMPORAL_SUVR"] = gen_random_population(mean1=1.199, sd1=0.132, size1=10000, mean2=1.799, sd2=0.548, size2=10000)
dict_random_tau_data["CTX_RH_INFERIORTEMPORAL_SUVR"] = gen_random_population(mean1=1.190, sd1=0.078, size1=10000, mean2=1.774, sd2=0.554, size2=10000)
dict_random_tau_data["CTX_LH_MIDDLETEMPORAL_SUVR"] = gen_random_population(mean1=1.161, sd1=0.130, size1=10000, mean2=1.671, sd2=0.523, size2=10000)
dict_random_tau_data["CTX_RH_MIDDLETEMPORAL_SUVR"] = gen_random_population(mean1=1.162, sd1=0.077, size1=10000, mean2=1.674, sd2=0.516, size2=10000)
dict_random_tau_data["CTX_LH_PRECENTRAL_SUVR"] = gen_random_population(mean1=0.997, sd1=0.070, size1=10000, mean2=1.139, sd2=0.264, size2=10000)
dict_random_tau_data["CTX_RH_PRECENTRAL_SUVR"] = gen_random_population(mean1=1.200, sd1=0.045, size1=10000, mean2=0.995, sd2=0.074, size2=10000) #Mimics inverted distribution
dict_random_tau_data["CTX_LH_POSTCENTRAL_SUVR"] = gen_random_population(mean1=0.972, sd1=0.074, size1=10000, mean2=1.084, sd2=0.252, size2=10000)
dict_random_tau_data["CTX_RH_POSTCENTRAL_SUVR"] = gen_random_population(mean1=1.091, sd1=0.286, size1=10000, mean2=1.091, sd2=0.286, size2=10000) #Mimics single distribution


for regions, regional_suvr in dict_random_tau_data.items():
    gm1, gm2, bic1, bic2 = gmm_calculation(regional_suvr)

    if regions == "CTX_RH_POSTCENTRAL_SUVR":
        gm_data = gmm_distribution_metrics(gm1, dist_2=False)
        figu = gmm_plot_distributions(regional_suvr, dict_gm=gm_data, name=f"{regions}", dist_2=False)
    else:
        gm_data = gmm_distribution_metrics(gm2, dist_2=True)
        figu = gmm_plot_distributions(regional_suvr, dict_gm=gm_data, name=f'{regions}', dist_2=True)
    

#Import CONP data
conp_ids = pd.read_csv("~/Desktop/participants_conp.tsv", sep='\t')

#Transform dictionary of simulated data to a dataframe
simulated_data = pd.DataFrame(data=dict_random_tau_data)

#Concatenate the ids with the data, ignoring the indices
final_simulated_data = conp_ids.merge(simulated_data, left_index=True, right_index=True, how="left")\
.set_index("participant_id")

#Save sheet
final_simulated_data.to_csv("/Users/fredericst-onge/Desktop/conp_simulated_tau-PET_data.csv")