""" Fingerprinting module

See SIHNPY documentation for more information on the functions of the script.

"""
import os
import numpy as np
import pandas as pd

def import_fingerprint_ids(id_list):
    """Function importing the list of IDs to analyse. We assume that the list of IDs are stored
    in either a .csv or .tsv file, or a text file with 1 ID per line.

    Parameters
    ----------
    id_list : str
        Path on the local computer to the file where the IDs are stored.

    Returns
    -------
    list
        Returns a list where each element is a participant ID.
    """

    #First, import the IDs. Assume the IDs are correct and in the first column only
    if id_list.endswith('.csv'):
        id_df = pd.read_csv(f'{id_list}', usecols=[0], index_col=0)
        id_ls = id_df.index.values

    elif id_list.endswith('.tsv'):
        id_df = pd.read_csv(f'{id_list}', sep='\t', usecols=[0], index_col=0,)
        id_ls = id_df.index.values

    else:
        id_arr = np.loadtxt(f'{id_list}', usecols=0)
        id_ls = id_arr.tolist()

    return id_ls

def _slice_matrix(nodes_index_within, matrix_file, nodes_index_between=None):
    """Internal function slicing matrices and returning "flattened" vectors.

    Parameters
    ----------
    nodes_index_between : list
        List of nodes to include in the fingerprinting calculation. If not interested in looking
        at between-network, the function defaults to calculating within-network. Defaults to None.
    nodes_index_within : list
        List of nodes to include in the fingerprinting calculation.
    matrix_file : numpy.array
        Array for a given participant comprising all the functional connectivity nodes.

    Returns
    -------
    numpy.array
        Returns a flattened array of the functional connectivity data.
    """

    if nodes_index_between:
        submatrix = matrix_file[nodes_index_within][:, nodes_index_between]
        #If between network, we force numpy to flatten the array to match the within-network input
        r_flat = submatrix.flatten()
    else:
        submatrix = matrix_file[nodes_index_within][:, nodes_index_within]
        #In the within-network, using np.triu_indices return by default a flat array.
        #We use triu_indices because the within-network matrix is symmetric. Including
        #the bottom half of the matrix would cause over-estimation of the correlation.
        r_flat = submatrix[np.triu_indices(len(submatrix), k=1)]

    return r_flat

def _norm_data(array_to_norm, norm=True):
    """Internal function normalizing (if necessary) the arrays before fingeprinting.

    Parameters
    ----------
    array_to_norm : numpy.array
        Raw sliced array to normalize.
    norm : bool, optional
        Whether or not the normalization should be applied, by default True

    Returns
    -------
    numpy.array
        Array with the chosen normalization applied to. Returns a copy of the array if no
        normalization is applied.
    """

    if norm is True:
        #By default, we apply a Fisher normalization.
        z1_norm = np.arctanh(array_to_norm)
    else:
        z1_norm = array_to_norm

    return z1_norm

class FingerprintMats:
    """Class object used to store information for the fingerprinting and to output
    the results of the fingerprinting analysis. This object is to be used when the
    input data is folders with 1 matrix per subject.
    """

    def __init__(self, id_ls, path_m1, path_m2):
        """Creates a FingerprintMats object made up of a list of ids, and the path to the data.

        Parameters
        ----------
        id_ls : list
            List of participants to fingerprint
        path_m1 : str
            Path (string) to the folder containing the participants
        path_m2 : _type_
            _description_
        """

        self.id_ls = id_ls #Final list of IDs to fingerprint
        self.path_m1 = path_m1 #Location of the first set of matrices (first modality)
        self.path_m2 = path_m2 #Location of the second set of matrices (second modality)

        #Create class objects for later
        self.num_sub = len(id_ls) #Number of subject included based on the ID list

        self.files_m1 = [] #Stores raw file names for first modality
        self.files_m2 = []
        self.final_m1 = [] #Stores file names where the individual is also in modality 2
        self.final_m2 = []
        self.similar_matrix = np.zeros(shape=(self.num_sub, self.num_sub))

        #Create empty dataframe to store the metrics
        self.coef_measures = pd.DataFrame(index=self.id_ls)

    def fetch_matrice_file_names(self):
        """Simple function importing the matrices as input for the fingerprinting computation.
        Does not require any argument (will use the path variables from the FingerprintMats
        objects).

        Raises
        ------
        OSError
            Checks whether the path exists and is able to import the file.
        """

        #First, find all the files in directories and store in a list
        try:
            for filename in os.listdir(self.path_m1):
                if os.path.isfile(f"{self.path_m1}/{filename}"):
                    self.files_m1.append(filename)

            for filename in os.listdir(self.path_m2):
                if os.path.isfile(f"{self.path_m2}/{filename}"):
                    self.files_m2.append(filename)
        except OSError as path_error:
            raise OSError from path_error

    def subject_selection(self, verbose=True):
        """Select participant files that are present in both modalities (i.e., intersection).
        The function assumes that the ID in the ID list will match in some way the file name
        in the folder (e.g., ID 6745 would match a matrix file named `6745.txt` or
        `part6745_rest.txt` or `6745`, but it will not match `674.txt`).

        Parameters
        ----------
        verbose : bool, optional
            Whether to print statements to the console or not, by default True
        """
        if verbose is True:
            print(f'We have {len(self.id_ls)} subjects in the list.')

        self.final_m1 = [filename for subject in self.id_ls
            for filename in self.files_m1 if subject in filename]
        self.final_m2 = [filename for subject in self.id_ls
            for filename in self.files_m2 if subject in filename]

        assert len(self.final_m1) == len(self.final_m2), "Final subject \
            lists from both modalities are not matching in length."
        assert ((len(self.final_m1) > 0) | (len(self.final_m2) > 0)), "Could not match subject IDs \
            from the list to any file."
        assert len(self.final_m1) == len(set(self.final_m1)), "Duplicate files detected for \
            modality 1."
        assert len(self.final_m2) == len(set(self.final_m2)), "Duplicate files detected for \
            modality 2"

        if verbose is True:
            print(f"We have in total {len(self.final_m1)} & {len(self.final_m2)} " +
            "participants with both modalities.")

    def _import_matrix(self, mod, i):
        """Internal function importing the matrices of interest from the local computer during
        the fingerprinting operation.

        Parameters
        ----------
        mod : int
            Integer (1 or 2) indicating which folder to fetch the folders from
        i : int
            Integer given by the loop in the fingerprint function. It identifies which list
            element we should import.

        Returns
        -------
        numpy.array
            Returns a numpy array containing the matrix of interest
        """
        if mod == 1:
            try:
                matrix_file = np.loadtxt(f'{self.path_m1}/{self.final_m1[i]}', dtype=np.double)
            except ValueError:
                matrix_file = np.loadtxt(f'{self.path_m1}/{self.final_m1[i]}',
                    delimiter=',', dtype=np.double)
        elif mod == 2:
            try:
                matrix_file = np.loadtxt(f'{self.path_m2}/{self.final_m2[i]}', dtype=np.double)
            except ValueError:
                matrix_file = np.loadtxt(f'{self.path_m2}/{self.final_m2[i]}',
                    delimiter=',', dtype=np.double)

        return matrix_file

    def fingerprint_mats(self, nodes_index_within, nodes_index_between=None,
    norm=True, corr_type="Pearson", verbose=True):
        """Core fingerprinting function. Takes every pair of matrices from modality 1 and 2
        and applies the fingerprint methodology between them.

        Parameters
        ----------
        nodes_index_within : int
            Integer representing the number of nodes to select. If nodes_index_between is not
            given, we assume we want to extract a symmetric sub-matrix (i.e., within-network).
        nodes_index_between : int, optional
            If requested, the matrix fed to the fingerprint can be asymetric, which is the case
            when wanting to do between-network fingerprinting, by default None
        norm : bool, optional
            _description_, by default True
        corr_type : str, optional
            _description_, by default "Pearson"
        verbose : bool, optional
            _description_, by default True
        """

        #For every participant, we need to correlate to every other participant.
        # We do this using a nested loop
        for i, sub in enumerate(self.id_ls):
            if verbose is True:
                print(f"Working on participant {i}: {sub}")

            #Imports the right matrix file
            matrix_file_m1 = self._import_matrix(1, i)
            #Slice and return the flat array of values to correlate
            r1_flat = _slice_matrix(matrix_file_m1, nodes_index_within, nodes_index_between)
            #If necessary, we normalize the data using Fisher's transformation
            z1_data = _norm_data(r1_flat, norm=norm)

            for j in (self.id_ls):
                matrix_file_m2 = self._import_matrix(2, j)
                r2_flat = _slice_matrix(matrix_file_m2, nodes_index_within, nodes_index_between)
                z2_data = _norm_data(r2_flat, norm=norm)

                #Correlate the array from the first subject to the array of the second subject
                if corr_type == "Pearson":
                    self.similar_matrix[i,j] = np.corrcoef(z1_data, z2_data)[0,1]

        #Fill lower triangle of the matrix for symmetry
        self.similar_matrix = self.similar_matrix + np.triu(self.similar_matrix, k=1).T

    def _fia_calculator(self):
        """Internal function computing the fingerprint identification accuracy,
        (number of correct identifications).

        Returns
        -------
        numpy.array
            Binary array for every participant included: a 1 indicates correct identification
            within the cohort and a 0 indicates incorrect identification.
        """

        fia_coef = np.empty(shape=self.num_sub)

        #For every row in the similarity matrix, if the maximum is achieved at the diagonal,
        # attribute a 1, otherwise a 0.
        for i in range(self.num_sub):
            if np.argmax(self.similar_matrix[i, :]) == i:
                fia_coef[i] = 1
            else:
                fia_coef[i] = 0

        return fia_coef

    def _si_calculator(self):
        """Internal function computing the self-identifiability (within-individual correlation).
        This is defined as the diagonal (within-individual correlations) of the similarity matrix.

        Returns
        -------
        numpy.array
            Returns an array containing the self-identifiability.
        """
        si_coef = np.diag(self.similar_matrix)

        return si_coef

    def _oi_calculator(self):
        """Internal function computing the others-identifiability (between-individual correlation).
        This is defined as the average of the off-diagonal elements (row-wise) of the similarity
        matrix.

        Returns
        -------
        numpy.array
            Returns an array containing the others-identifiability.
        """
        oi_coef = (self.similar_matrix.sum(1)-np.diag(self.similar_matrix))\
        /self.similar_matrix.shape[1]-1

        return oi_coef

    def _identif_calculator(self, si_coef, oi_coef):
        """Internal function computing the differential identifiability metric 
        from Amico and Goni (2018). This is simply the substraction of the diagonal and average
        off-diagonal elements from the similarity matrix.

        Parameters
        ----------
        si_coef : numpy.array
            Array containing the fingerprinting coefficient.
        oi_coef : numpy.array
            Array containing the alikeness coefficient.

        Returns
        -------
        numpy.array
            Returns an array containing the differential identifiability.
        """

        diff_ident = si_coef - oi_coef

        return diff_ident

    def fp_metrics_calc(self, name):
        """Method computing the different fingerprint metrics and stores them in a dataframe
        for export. Each metric is computed and stored in a numpy.array which are then used
        to populate the dataframe.

        Parameters
        ----------
        name : str
            String to add to the variables. This is so the user can differentiate the different
            runs of the fingerprinting if multiple are used.

        Returns
        -------
        pandas.DataFrame
            Returns a pandas.DataFrame containing 5 columns: the ID and each of the four metrics.
        """

        #Compute the different metrics
        fia_coef = self._fia_calculator()
        si_coef = self._si_calculator()
        oi_coef = self._oi_calculator()
        diff_identif_coef = self._identif_calculator(si_coef, oi_coef)

        #Create a dictionary and store the measures
        coef_dict = {f"si_{name}":si_coef,
                    f"oi_{name}":oi_coef,
                    f"fia_{name}":fia_coef,
                    f"di_{name}":diff_identif_coef}

        #Create a dataframe from the dictionary and merge it to the original dataframe
        self.coef_data = pd.concat([self.coef_data, pd.DataFrame(coef_dict)], axis=1,
            ignore_index=True)
        self.coef_data.index.name = "ID"

        assert coef_dict[f"{si_coef}"].isnull().sum() == 0, "Error: some subjects have \
            missing values from final dataframe"

    def fp_mat_export(self, output_path, name, out_full=True, dir_struct=True):
        """Export the fingerprinting output to file. What is outputted and how is user
        dependant. By default, exports the similarity matrix, the subject list and the
        computed fingerprint metrics, and creates separate dictories for the similarity
        matrix and the subject list.

        Parameters
        ----------
        output_path : str
            Path where all the fingerprinting output should go.
        name : str
            String to add to the file names
        out_full : bool, optional
            Whether we want the similarity matrix and subject list to be outputted, by default True
        dir_struct : bool, optional
            Whether we want similarity matrix and subject list to have their own directory, by
            default True
        """

        assert os.path.exists(output_path), "Error: Path for output doesn't exist."

        path_fp_final = f'{output_path}/{name}'
        if not os.path.exists(path_fp_final):
            os.makedirs(path_fp_final)

        self.coef_data.to_csv(f"{path_fp_final}/fp_metrics_{name}.csv")

        #If we want to output the similarity matrices and the subject lists too...
        if out_full is True:
            #We output ALL the elements of the fingerprinting (similarity matrix, subject_list
            #  and fingerprint measures)
            if dir_struct is True:
                #If we do a full directory structure, we want to output all the elements to
                # separate directories
                dir_sym = f"{path_fp_final}/similarity_matrices"
                dir_sub = f"{path_fp_final}/subject_list"

                if not os.makedirs(dir_sym):
                    os.makedirs(dir_sym)
                if not os.makedirs(dir_sub):
                    os.makedirs(dir_sym)

                np.savetxt(f"{dir_sym}/similarity_matrix_{name}.csv", self.similar_matrix,
                    delimiter=",")
                np.savetxt(f"{dir_sub}/subject_list_{name}.csv", self.id_ls,
                    delimiter="\n")
            else:
                np.savetxt(f"{path_fp_final}/similarity_matrix_{name}.csv", self.similar_matrix,
                    delimiter=",")
                np.savetxt(f"{path_fp_final}/subject_list_{name}.csv", self.id_ls,
                    delimiter="\n")
