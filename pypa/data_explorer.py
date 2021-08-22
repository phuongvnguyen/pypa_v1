"""
This module is to do the Exploratory Data Analysis (EDA)
Authored: Phuong V. Nguyen
Dated: August 21th, 2021
"""
import pandas as pd
import numpy as np
import dataset_calling
from IPython.display import display, HTML, clear_output, update_display


def profile(data):
    """
    This function is to do EDA
    :param data: data input
    """
    import pandas_profiling
    print('\033[1m' + 'Data types and null:' + '\033[0m')
    print(data.info())
    print('\033[1m' + 'Descriptive statistics' + '\033[0m')
    display(data.describe())
    pf = pandas_profiling.ProfileReport(data)
    display(pf)

# class eda(object):
#
#     def __init__(self, data):
#         self.data = data
#         self.prof = self.profile(self.data)
#
#     def profile(self, data_for_profiling):
#         import pandas_profiling
#         pf = pandas_profiling.ProfileReport(data_for_profiling)
#         display(pf)
#         return pf
#
#
# class main(object):
#     eda = eda(data)
#
#
# if __name__ == '__main__':
#     main()
