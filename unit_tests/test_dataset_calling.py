import os, sys

sys.path.insert(0, os.path.abspath(".."))

import pandas as pd
import pytest
import pypa.dataset_calling


def test():
    # loading dataset
    credit = pypa.dataset_calling.get_data("credit")
    assert isinstance(credit, pd.core.frame.DataFrame)
    row, col = credit.shape
    assert row == 24000
    assert col == 24
    assert credit.size == 576000
    assert 1 == 1


if __name__ == "__main__":
    test()
