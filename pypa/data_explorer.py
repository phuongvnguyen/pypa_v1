"""
This module is to do the Exploratory Data Analysis (EDA)
Authored: Phuong V. Nguyen
Dated: August 21th, 2021
"""
import pandas as pd
import numpy as np
import pypa.dataset_calling
from IPython.display import display, HTML, clear_output, update_display


def investor(data,
            feature,
            label,
            profile=False,
            sweetplot=False,
            autoplot=False,
            dtale=False
            ):
    """
    This function is do EAD both descriptive statistics and visualization
    :param data:
    :param feature: list of features
    :param label: target variable
    :param profile: using pandas-profiling
    :param sweetplot: using sweetvis
    :param autoplot: using autovis
    :param dtale: using D-tale
    :return state: result of EDA
    """
    # print('\033[1m' + 'Data types and nullit:' + '\033[0m')
    # print(data.info())
    # print('\033[1m' + 'Descriptive statistics' + '\033[0m')
    # display(data.describe())
    if profile:
        import pandas_profiling
        pf = pandas_profiling.ProfileReport(data)
        display(pf)
        state = 'EDA WITH PROFILE IS DONE'
    elif sweetplot:
        import sweetviz
        my_report = sweetviz.analyze([data, 'Train'],
                                     target_feat=label)
        my_report.show_html('FinalReport.html')
        state = 'EDA WITH SWEETPLOT IS DONE'
    else:
        if autoplot:
            from autoviz.AutoViz_Class import AutoViz_Class
            AV = AutoViz_Class()
            df = AV.AutoViz(data)
            print('Sorry, this task is under construction')
        elif dtale:
            import dtale
            d = dtale.show(data)
            d.open_browser()
            state = 'EDA WITH D-TALE IS DONE'
    return state



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
