from importlib import resources

def get_fingerprint_simulated_data():
    """Simple function returning the paths to a .csv file and to two paths of simulated
    functional connectivity datasets.

    Returns:
        str: Returns three strings representing the three input paths for
        the fingerprinting.
    """

    list_paths = []
    for paths in ["fp_simulated_id_list.csv", "matrices_simulated_mod1", "matrices_simulated_mod2"]:
        with resources.files(f"sihnpy.data.fingerprinting") as f:
            list_paths.append(f"{str(f)}/{paths}")
    print(list_paths[0])
    print(list_paths[1])
    print(list_paths[2])
    
    return list_paths[0], list_paths[1], list_paths[2]
