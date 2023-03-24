from sihnpy import datasets
from sihnpy import spatial_extent as spex
import numpy as np

tau_data, regional_averages, regional_thresholds = datasets.pad_spex_input()

#Get the data to keep only the ID column (as index) and the SUVR
red_data = tau_data.set_index('participant_id').drop(labels=['sex', 'test_language', 'handedness_score', 'handedness_interpretation'], axis=1)

#gm_objects, clean_data = spex.gmm_estimation(red_data, fix=False)

#list_test = [0.3, 0.6, 0.1, 0.2]
#list_test
#list_test.sort()

#################### Test spatial extent code

#Step 1 - GMM Estimation
gm_objects, clean_data = spex.gmm_estimation(red_data, fix=True)

#Step 2 - GMM measures
final_data, final_gm_dict, gmm_measures = spex.gmm_measures(cleaned_data=clean_data, gm_objects=gm_objects, fix=True)

#Step 3 - GMM Probabilities
probability_df = spex.gmm_probs(final_data=final_data, final_gm_dict=final_gm_dict)

#probability_df.to_csv("/Users/fredericst-onge/Desktop/prob_tests.csv")
#final_data.to_csv("/Users/fredericst-onge/Desktop/suvr_tests.csv")

#Step 4 (Optional) - Histograms
#dict_fig_hist = spex.gmm_histograms(final_data=final_data, gmm_measures=gmm_measures, probs_df=probability_df, dist_2=True, type="all")

#dict_fig_hist['hist_density_CTX_LH_FUSIFORM_SUVR']
#dict_fig_hist['hist_raw_CTX_LH_FUSIFORM_SUVR']

#Step 5 - Thresholds derivation
thresh_df = spex.gmm_threshold_deriv(final_data=final_data, probs_df=probability_df, prob_threshs=[0.5, 0.9], improb=1.0)

#Step 6 (Optional) - Export

#Step 7 - 

print((final_data['CTX_RH_MIDDLETEMPORAL_SUVR'] >= 0.761154).sum()) #307
print((final_data['CTX_RH_MIDDLETEMPORAL_SUVR'] >= 1.439846).sum()) #74

