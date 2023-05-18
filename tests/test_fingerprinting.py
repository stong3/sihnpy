import os
import math 
import numpy as np
import pandas as pd
import pytest

from sihnpy import fingerprinting as s_fp
from sihnpy import datasets

def test_import_fingerprint_ids():
    """Function testing the import of the fingerprinting IDs
    """

    data_ids_csv = "tests/test_data/fingerprinting/id_list.csv"
    data_ids_tsv = "tests/test_data/fingerprinting/id_list.tsv"
    data_ids_txt = "tests/test_data/fingerprinting/id_list.txt"

    id_ls_csv = s_fp.import_fingerprint_ids(data_ids_csv)
    id_ls_tsv = s_fp.import_fingerprint_ids(data_ids_tsv)
    id_ls_txt = s_fp.import_fingerprint_ids(data_ids_txt)

    assert len(id_ls_csv) == 10, "There should be 10 participants in the test data (csv)."
    assert len(id_ls_tsv) == 10, "There should be 10 participants in the test data (tsv)."
    assert len(id_ls_txt) == 10, "There should be 10 participants in the test data (txt)."
    assert ["01a", "02a", "03a", "04a", "05a", "06a", "07a", "08a", "09a", "10a"] == id_ls_csv, "\
        Participants on the list are not in the imported data."

def test_fetch_matrix_file_names():
    """ Testing the fetch_matrix_file_names method of the FingerprintMats class
    """
    #List of IDs in the test data
    id_ls = ["01a", "02a", "03a", "04a", "05a", "06a", "07a", "08a", "09a", "10a"]

    #instantiate object
    fp_object = s_fp.FingerprintMats(id_ls=id_ls,
        path_m1="tests/test_data/fingerprinting/matrices_mod1",
        path_m2="tests/test_data/fingerprinting/matrices_mod2")

    #Get file names
    files_m1_test, files_m2_test = fp_object.fetch_matrix_file_names()

    #Check right number of files
    assert len(files_m1_test) == 10, "Modality 1 doesn't have the right number of files \
        (should be 10)"
    assert len(files_m2_test) == 8, "Modality 2 doesn't have the right number of files \
        (should be 8)"

    #Check that OSError is raised when path doesn't exist.
    with pytest.raises(OSError):
        fp_object.path_m1 = "obviously/not/the/right/path"
        fp_object.path_m2 = "i/mean/im/not/even/trying"
        fp_object.fetch_matrix_file_names()

def test_subject_selection():
    """ Testing the subject_selection method of the FingerprintMats class
    """
    #List of IDs in the test data
    id_ls = ["01a", "02a", "03a", "04a", "05a", "06a", "07a", "08a", "09a", "10a"]
    id_expected = ["01a", "03a", "04a", "05a", "06a", "07a", "09a", "10a"]

    #instantiate object
    fp_object = s_fp.FingerprintMats(id_ls=id_ls,
        path_m1="tests/test_data/fingerprinting/matrices_mod1",
        path_m2="tests/test_data/fingerprinting/matrices_mod2")

    #File names
    files_m1 = ['mat_01a.txt', 'mat_02a.txt', 'mat_03a.txt', 'mat_04a.txt', 'mat_05a.txt',
        'mat_06a.txt', 'mat_07a.txt', 'mat_08a.txt', 'mat_09a.txt', 'mat_010a.txt']
    files_m2 = ['mat_01a.txt', 'mat_03a.txt', 'mat_04a.txt', 'mat_05a.txt',
        'mat_06a.txt', 'mat_07a.txt', 'mat_09a.txt', 'mat_010a.txt']

    sub_final, final_m1_test, final_m2_test = fp_object.subject_selection(files_m1=files_m1,
        files_m2=files_m2)

    assert len(final_m1_test) == 8, "Modality 1 doesn't have the right number of files \
        (should be 8)"
    assert len(final_m2_test) == 8, "Modality 2 doesn't have the right number of files \
        (should be 8)"
    assert id_expected == sub_final, "Participants retained don't match the expected list."

def test_subject_selection_error_raising():
    """ Testing the subject_selection method of the FingerprintMats class. Specifically testing if the errors raise properly.
    """
    #Prep input
    id_ls = ["01a", "02a", "03a", "04a", "05a", "06a", "07a", "08a", "09a", "010a"]
    fp_object = s_fp.FingerprintMats(id_ls=id_ls,
        path_m1="tests/test_data/fingerprinting/matrices_mod1",
        path_m2="tests/test_data/fingerprinting/matrices_mod2")

    #Error raising tests
    with pytest.raises(SystemExit):
        files_m1 = []
        files_m2 = ['mat_01a.txt']
        fp_object.subject_selection(files_m1=files_m1,
            files_m2=files_m2)

    with pytest.raises(SystemExit):
        files_m1 = ['mat_01a.txt', 'mat_01a.txt', 'mat_03a.txt']
        files_m2 = ['mat_01a.txt', 'mat_02a.txt', 'mat_03a.txt']
        fp_object.subject_selection(files_m1=files_m1,
            files_m2=files_m2)

    with pytest.raises(SystemExit):
        files_m1 = ['mat_01a.txt', 'mat_02a.txt', 'mat_03a.txt']
        files_m2 = ['mat_01a.txt', 'mat_01a.txt', 'mat_03a.txt']
        fp_object.subject_selection(files_m1=files_m1,
            files_m2=files_m2)

def test_fingerprint_mats_nodes_within():
    """ Testing the fingerprint_mats function, using "within-network" edges. 
    """
    id_ls = ["01a", "02a", "03a", "04a", "05a", "06a", "07a", "08a", "09a", "10a"]
    fp_object = s_fp.FingerprintMats(id_ls=id_ls,
        path_m1="tests/test_data/fingerprinting/matrices_mod1",
        path_m2="tests/test_data/fingerprinting/matrices_mod2")

    fp_object.sub_final = ["01a", "03a", "04a", "05a"]
    fp_object.final_m1 = ['mat_01a.txt', 'mat_03a.txt', 'mat_04a.txt', 'mat_05a.txt']
    fp_object.final_m2 = ['mat_01a.txt', 'mat_03a.txt', 'mat_04a.txt', 'mat_05a.txt']

    #Assume we take the whole brain for the tests. We created a smaller 100 version
    nodes_index_within = list(range(0, 100))

    similar_matrix = fp_object.fingerprint_mats(nodes_index_within=nodes_index_within)

    #Assertions
    assert similar_matrix.shape == (len(fp_object.sub_final), len(fp_object.sub_final)), "Similarity matrix is not the right shape (should be 4x4)"

    assert round(similar_matrix[0,0], 1) == pytest.approx(1.0), "Self-identifiability in the matrix should be near perfect (1)."

def test_fp_metrics_calc():
    """ Testing the fp_metrics_calc method
    """
    #To test this function, we need a similarity matrix
    similar_matrix = np.array([
        [1, 0.00387545, -0.00856911, -0.01271971], 
        [0.0077509, 1., 0.01608879, 0.0183433],
        [-0.01713821, 0.03217759, 1., -0.0038769],
        [-0.02543943, 0.0366866, -0.0077538, 1.]])
    
    id_ls = ["01a", "02a", "03a", "04a", "05a", "06a", "07a", "08a", "09a", "10a"]
    fp_object = s_fp.FingerprintMats(id_ls=id_ls,
        path_m1="tests/test_data/fingerprinting/matrices_mod1",
        path_m2="tests/test_data/fingerprinting/matrices_mod2")

    fp_object.sub_final = ["01a", "03a", "04a", "05a"]
    
    #Test the function
    coef_data = fp_object.fp_metrics_calc(similar_matrix=similar_matrix, name='test')
    print(coef_data)

    assert coef_data.index.name == "ID", "Index name doesn't set properly."
    assert coef_data.loc['01a', 'si_test'] == pytest.approx(1.0), "Self-identifiability is not giving the right result."
    assert coef_data.loc['03a', 'oi_test'] == pytest.approx(0.014061), "Others-identifiability is not giving the right result."
    assert coef_data.loc['04a', 'fia_test'] == pytest.approx(1.0), "Fingerprint identifiability is not giving the right result."
    assert coef_data.loc['05a', 'di_test'] == pytest.approx(0.998836), "Differential identifiability is not giving the right result."

def test_integration_fp_mats():
    """ Testing the integration of functions and methods to run
    the fingerprint analysis.
    """

    id_ls_csv = s_fp.import_fingerprint_ids("tests/test_data/fingerprinting/id_list.csv")

    assert isinstance(id_ls_csv, list), "Imported list of IDs should be a list."
    assert len(id_ls_csv) == 10, "Imported list of IDs should have 10 people"

    fp_object = s_fp.FingerprintMats(id_ls=id_ls_csv,
        path_m1="tests/test_data/fingerprinting/matrices_mod1",
        path_m2="tests/test_data/fingerprinting/matrices_mod2")

    assert fp_object.id_ls == id_ls_csv, "Object creation is not done properly (wrong list of IDs is added to the object."
    assert fp_object.path_m1 == "tests/test_data/fingerprinting/matrices_mod1", "Object creation is not done properly (wrong list of IDs is added to the object."

    files_m1, files_m2 = fp_object.fetch_matrix_file_names()

    assert len(files_m1) == 10, "Wrong number of files for modality 1"
    assert len(files_m2) == 8, "Wrong number of files for modality 2"

    sub_final, final_m1, final_m2 = fp_object.subject_selection(files_m1=files_m1, files_m2=files_m2)

    assert len(sub_final) == 8, "Wrong number of participants selected as final participants"
    assert len(final_m1) == 8, "Wrong number of files for modality 1"
    assert len(final_m2) == 8, "Wrong number of files for modality 2 (final)"

    similar_matrix = fp_object.fingerprint_mats(nodes_index_within=list(range(0, 100)))

    assert similar_matrix.shape == (8,8), "Similarity matrix is not the right shape (should be 8x8)"
    assert similar_matrix[0,0] == pytest.approx(1.0), "Calculated metrics are incorrect (diagonal should be 1.0 in the test data)."

    fp_coefs = fp_object.fp_metrics_calc(similar_matrix=similar_matrix, name="test")

    assert len(fp_coefs) == 8, "Number of participants computed should be 8."

    fp_object.fp_mat_export(output_path="tests/test_data/fingerprinting/output", coef_data=fp_coefs, similar_matrix=similar_matrix, name='test')

    assert os.path.exists("tests/test_data/fingerprinting/output"), "Export function didn't create the output folder as expected."
    assert os.path.exists("tests/test_data/fingerprinting/output/test/fp_metrics_test.csv"), "Export function didn't export FP metrics."
    assert os.path.exists("tests/test_data/fingerprinting/output/test/similarity_matrices"), "Export function didn't create a folder for similarity matrices."
    assert os.path.exists("tests/test_data/fingerprinting/output/test/subject_list"), "Export function didn't create a folder for subject lists."

@pytest.fixture
def data_fp_tab_import():
    """ Creates the data use for tests
    """

    volume_data = datasets.pad_fptab_input()[0]

    return volume_data

@pytest.fixture
def data_fingerprint_tabs():
    """ Creates the data to use for the fingerprinting tabular data.
    """

    volume_data = datasets.pad_fptab_input()[0]
    data_bl, data_fu = s_fp.import_fingerprint_data(data=volume_data, var='session')

    return data_bl, data_fu

@pytest.fixture
def data_fingerprint_metrics():
    """ Creates the data to use for testing the fingerprint metrics function.
    """

    volume_data = datasets.pad_fptab_input()[0]
    data_bl, data_fu = s_fp.import_fingerprint_data(data=volume_data, var='session')
    similarity_matrix = s_fp.fingerprint_tabs(data1=data_bl, data2=data_fu, pref='ctx')

    return data_bl, similarity_matrix

def test_import_fingerprint_data(data_fp_tab_import):
    """ Test the import and clean of the data
    """

    data_bl, data_fu = s_fp.import_fingerprint_data(data=data_fp_tab_import, var='session')

    assert len(data_bl) == 234, "Wrong number of rows for bl data"
    assert len(data_bl.columns.values) == 70, "Wrong number of columns for bl data"
    assert len(data_fu) == 234, "Wrong number of rows for fu data"
    assert len(data_fu.columns.values) == 70, "Wrong number of columns for fu data"
    assert data_bl.iloc[0,2] == 1768.0, "Rows are not in the right order for bl data"
    assert data_fu.iloc[0,2] == 1845.0, "Rows are not in the right order for bl data"

    assert data_bl.index.values.all() == data_fu.index.values.all(), "Index of the two datasets do not match. Won't fingerprint."

def test_fingerprint_tabs(data_fingerprint_tabs):
    """ Test the creation of the similarity matrix
    """

    data_bl, data_fu = data_fingerprint_tabs

    similarity_matrix = s_fp.fingerprint_tabs(data1=data_bl, data2=data_fu, pref='ctx')

    assert np.shape(similarity_matrix) == (234, 234), "Shape of similarity matrix is not 234x234"
    assert math.isclose(similarity_matrix[0,0], 0.9993991493256379), "Wrong number in similarity matrix for SI"
    assert math.isclose(similarity_matrix[0,1], 0.9668773975353411), "Wrong number in similarity matrix for OI (1)"
    assert similarity_matrix[0,1] == similarity_matrix[1,0], "Similarity matrix is not mirrored in the lower triangle"


def test_tab_metrics_calc(data_fingerprint_metrics):
    """ Test the computation of the fingerprint metrics.
    """
    data_bl, similar_matrix = data_fingerprint_metrics

    fp_metrics = s_fp.tab_metrics_calc(data=data_bl, similar_matrix=similar_matrix, name='test')

    assert len(fp_metrics) == len(data_bl), "The fp_metrics doesn't have the right number of participants"
    assert math.isclose(fp_metrics.iloc[0,0], 0.9993991493256379), "The SI of the first participant is not right"
    assert math.isclose(fp_metrics.iloc[233,3], 0.018491580529617635), "The DI of the last participant is not right"