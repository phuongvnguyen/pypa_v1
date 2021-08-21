import pandas as pd
import numpy as np
import pypa.dataset_calling as data_call

credit = data_call.get_data("credit", profile=False)