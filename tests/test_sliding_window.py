import pandas as pd
import pytest
import math

from sihnpy import sliding_window as sw

@pytest.fixture
def data_bins():
    """ Define the data necessary to test the bins and build_window functions.
    """
    return pd.read_csv("tests/test_data/sliding_window/test_age_data.csv", index_col=0)

def test_bins(data_bins):
    """ Function testing the computing bins function
    """

    n_windows_1_no_collapse = sw.bins(data=data_bins, var='age', w_size=100, s_size=20, collapse=False)

    n_windows_2_no_collapse = sw.bins(data=data_bins, var='age', w_size=108, s_size=20, collapse=False)

    n_windows_1_collapse = sw.bins(data=data_bins, var='age', w_size=100, s_size=20, collapse=True)

    n_windows_2_collapse = sw.bins(data=data_bins, var='age', w_size=108, s_size=20, collapse=True)

    assert n_windows_1_no_collapse == 12, "Wrong number of windows. Should be 12 for 1st parameter no collapse"
    assert n_windows_2_no_collapse == 11, "Wrong number of windows. Should be 11 for 2nd parameter no collapse"
    assert n_windows_1_collapse == 11, "Wrong number of windows. Should be 11 for 1st parameter with collapse"
    assert n_windows_2_collapse == 10, "Wrong number of windows. Should be 10 for 2nd parameter with collapse"

def test_build_windows(data_bins):
    """ Function testing the computing of the build_windows function
    """

    w_store = sw.build_windows(data=data_bins, var='age', w_size=100, s_size=20, n_bin=11)

    assert len(w_store) == 11, "Wrong number of windows after building."
    assert w_store['ww100_sts20_w01'].index.get_loc('sub-7755697') == 99, "Index is not sorted as expected in first window."
    assert w_store['ww100_sts20_w05'].index.get_loc('sub-7755697') == 19, "Index is not sorted as expected in the fifth window."
    assert len(w_store['ww100_sts20_w11'].index.values) == 108, "Last window should have 108 participants"

def test_data_by_window(data_bins):
    """ Function testing the computing of the data reconstruction
    """

    w_store = sw.build_windows(data=data_bins, var='age', w_size=100, s_size=20, n_bin=11)

    w_data = sw.data_by_window(w_store=w_store, data=data_bins)

    assert len(w_data) == 11, "Wrong number of windows after reconstructing."
    assert len(w_data['ww100_sts20_w01'].columns.values) == 5, "Wrong number of columns after reconstructing."
    assert w_data['ww100_sts20_w01'].index.get_loc('sub-7755697') == 99, "Index is not sorted as expected in first window."
    assert w_data['ww100_sts20_w05'].index.get_loc('sub-7755697') == 19, "Index is not sorted as expected in the fifth window."
    assert len(w_data['ww100_sts20_w11'].index.values) == 108, "Last window should have 108 participants"

def test_sum_by_window(data_bins):
    """ Function testing the computing of the data statistics. 
    """

    w_store = sw.build_windows(data=data_bins, var='age', w_size=100, s_size=20, n_bin=11)

    w_data = sw.data_by_window(w_store=w_store, data=data_bins)

    w_summary = sw.sum_by_window(w_data=w_data, var='age')

    assert len(w_summary) == 11, "Wrong number of windows"
    assert len(w_summary.columns.values) == 5, "Wrong number of metrics computed"
    assert math.isclose(w_summary.loc['ww100_sts20_w01', 'mean_age'], 59.457366, rel_tol=1e-6), "Wrong average for age of the first window"
    assert math.isclose(w_summary.loc['ww100_sts20_w10', 'max_age'], 72.391602, rel_tol=1e-6), "Wrong maximum age age of the 10th window"