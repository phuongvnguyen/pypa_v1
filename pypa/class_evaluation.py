"""
This module is to evaluate the performance of classification models
Authored: Phuong V. Nguyen
Dated: August 24th, 2021
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve


def calibration_eval(y_test, y_pred_prob, nbins):
    """
    this function is to evaluate the performance of classification model
    in terms of classification
    :param y_test: target
    :param y_pred_prob: predicted prob. target
    :param nbins: number of bins
    :return:
    """
    fop, mpv = calibration_curve(y_test, y_pred_prob,
                                 n_bins=nbins, normalize=True)
    # plot perfectly calibrated
    plt.plot([0, 1], [0, 1], linestyle='--')
    # plot model reliability
    plt.plot(mpv, fop, marker='.')
    plt.show()

def calibration(actual_val, pred_prob,levels):
    """
    This function is to estimate the conversion rate by using gain table
    :param actual_val: actual value of output
    :param pred_prob: predicted prob. of output
    :param levels: the bins
    :return pdt2: table shows conversion rate by quantiles
    """
    pdt = pd.DataFrame({'label': actual_val['LABEL'], 'predict': pred_prob})
    pdt['level'], bins = pd.qcut(pdt['predict'], 5, labels=levels, duplicates='raise', retbins=True)
    pdt2 = pdt.groupby(['level']).agg(label_count=('label', 'count'),
                                      label_sum=('label', 'sum'),
                                      level_min=('predict', 'min'),
                                      level_max=('predict', 'max')
                                      ) \
        .reset_index() \
        .sort_values('level', ascending=False)
    pdt2['conversion_rate'] = pdt2['label_sum'] / pdt2['label_count']
    return pdt2
# label_levels= ['Level1','Level2','Level3','Level4','Level5']
# cr = calibration(y_test,y_pred_prob,label_levels)
# cr
