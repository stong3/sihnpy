""" Script generating simulated data for the sliding-window module

Quick script generating simulated data to test the sliding-window functionalities.
We want to create 1 variable (age) from Gaussian noise. That's it.
"""

import pandas as pd
from scipy import stats
import numpy as np

def gen_random_population(mean, sd, size):
    """_summary_

    Parameters
    ----------
    mean : float
        Mean of the distribution
    sd : float
        _description_
    size : _type_
        _description_

    Returns
    -------
    numpy.array
        Numpy array containing the 308 random data points
    """
    np.random.seed(667)
    pop_sim_data = np.random.choice(stats.norm.rvs(mean, sd, size, random_state=667), 308)

    return np.where(pop_sim_data < 55, 55, pop_sim_data)

#Import CONP data
conp_ids = pd.read_csv("~/Desktop/participants_conp_corr.tsv", sep='\t', index_col=0)

#Create the age column. In PREVENT-AD Open, the mean age is 65 and SD is 5 (based on Tremblay-Mercier 2021)
conp_ids['age'] = gen_random_population(65, 5, 10000) #Inclusion criteria states nothing lower than 55 is allowed in PREVENT-AD. We force anyone under 55 to actually be 55 just to make sure we respect the original data.

conp_ids['age'].mean() #Check the mean. 65.31 years. Check!
conp_ids['age'].std() #Check the SD. 5.18 years. Check!

#Save sheet
conp_ids.to_csv("~/Desktop/conp_simulated_age_data.csv")