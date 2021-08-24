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
