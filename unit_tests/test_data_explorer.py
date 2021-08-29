import os, sys

sys.path.insert(0, os.path.abspath(".."))

import pandas as pd
import pytest
import pypa.dataset_calling
from pypa.data_explorer import investor


def test():
    # loading dataset
    credit = pypa.dataset_calling.get_data("credit")
    eda = investor(credit, feature=credit.columns[0:10], label='default',
                   dtale=True)
    assert eda == 'EDA WITH D-TALE IS DONE'


if __name__ == "__main__":
    test()
