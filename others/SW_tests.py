from sihnpy import datasets
from sihnpy import sliding_window as sw

data_age = datasets.pad_sw_input()

n_bins_age_clean = sw.bins(data=data_age, var="age", w_size=108, s_size=20)

n_bins_age_unclean = sw.bins(data=data_age, var='age', w_size=100, s_size=20)

w_store_clean = sw.build_windows(data=data_age, var='age', w_size=108, s_size=20, n_bin=n_bins_age_clean)

w_store_unclean = sw.build_windows(data=data_age, var='age', w_size=100, s_size=20, n_bin=n_bins_age_unclean)

w_store_clean['ww108_sts20_w01'] #Seems right length
# The last participant in the window is sub-6794127
# Based on the window and step size, we expect this participant to show up in 6 windows (position 108 (w01) - (88) 20 (w02) - (68) 20 (w03) - (48) 20 (w04) - (28) 20 (w05) - (8) 20 (w06))

if "sub-6794127" in w_store_clean['ww108_sts20_w07'].index.values:
    print(True)

w_store_clean['ww108_sts20_w01'].index.get_loc("sub-6794127") #107
w_store_clean['ww108_sts20_w02'].index.get_loc("sub-6794127") #87

w_data_clean = sw.data_by_window(w_store=w_store_clean, data=data_age)

#Check that the final data is correct (sorted)
w_data_clean['ww108_sts20_w01']['age'].is_monotonic
w_data_clean['ww108_sts20_w01']['age'].min() == w_data_clean['ww108_sts20_w01']['age'].iloc[0]
w_data_clean['ww108_sts20_w01']['age'].max() == w_data_clean['ww108_sts20_w01']['age'].iloc[107]

w_data_unclean = sw.data_by_window(w_store=w_store_unclean, data=data_age)

w_summary_clean = sw.sum_by_window(w_data=w_data_clean, var='age')

sw.export_data(w_data=w_data_clean, w_summary=w_summary_clean, var='age', path="/Users/fredericst-onge/Desktop/window_test", name='test_window')