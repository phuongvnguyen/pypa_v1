"""
This module is to do feature engineer.
Authored: Phuong V. Nguyen
Dated: August 21th, 2021
"""
import pandas as pd
import numpy as np
import ipywidgets as wg
from IPython.display import display
from ipywidgets import Layout
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.impute._base import _BaseImputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import QuantileTransformer


def basic_feat_engineer(data, features_to_drop):
    """
    this function is to do some basic aspects of feature engineer
    :param data: input data
    :param features_to_drop: list of features were asked to drop
    :return df: cleaned data
    """

    df = data.copy()

    # also make sure that all the column names are string
    df.columns = [str(i) for i in df.columns]

    # drop any columns that were asked to drop
    df.drop(columns=features_to_drop, errors="ignore", inplace=True)

    # if there are inf or -inf then replace them with NaN
    df.replace([np.inf, -np.inf], np.NaN, inplace=True)

    # if data type is bool or pandas Categorical , convert to categorical
    for i in df.select_dtypes(include=["bool", "category"]).columns:
        df[i] = df[i].astype("object")

    # wiith csv , if we have any null in  a colum that was int , panda will read it as float.
    # so first we need to convert any such floats that have NaN and unique values are
    # lower than 20
    for i in df.select_dtypes(include=["float64"]).columns:
        df[i] = df[i].astype("float32")
        # count how many Nas are there
        na_count = sum(data[i].isnull())
        # count how many digits are there that have decimiles
        count_float = np.nansum(
            [False if r.is_integer() else True for r in data[i]]
        )
        # total decimiels digits
        count_float = (
                count_float - na_count
        )  # reducing it because we know NaN is counted as a float digit
        # now if there isnt any float digit , & unique levales are less than
        # 20 and there are Na's then convert it to object
        if (count_float == 0) & (df[i].nunique() <= 20) & (na_count > 0):
            df[i] = df[i].astype("object")

    return df
