"""
module: datset_calling is to import dataset
authored: Phuong V. Nguyen
dated: August 20th, 2021
"""


def get_data(name_dataset='index',
             profile=False,
             verbose=True,
             address="../datasets/",):
    """
    This function is to load dataset from the git repository
    :param name_dataset: name of dataset (str)
    :param profile: bool, default = False
        When set to true, an interactive EDA report is displayed.
    :param verbose:
    :param address: url of dataset in the git repo
    :return data: loaded dataset (pandas.DataFrame)
    """
    import pandas as pd
    import os.path
    from IPython.display import display, HTML, clear_output, update_display

    extension = ".csv"
    filename = str(name_dataset) + extension
    full_address = address + filename
    # loading data
    # if os.path.isfile(filename):
    #     data = pd.read_csv(filename)
    # else:
    #     data = pd.read_csv(full_address)
    data = pd.read_csv(full_address)

    # create a copy for pandas profiler
    data_for_profiling = data.copy()

    if profile:
        import pandas_profiling
        pf = pandas_profiling.ProfileReport(data_for_profiling)
        display(pf)
    else:
        if verbose:
            display(data.head())

    return data
