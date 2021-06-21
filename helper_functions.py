import os
import numpy as np
import urllib.request
import tarfile
import pandas as pd
import pathlib

# Collecting the data
DOWNLOAD_ROOT = "https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.tgz"
PATH = pathlib.Path().cwd()
DATA_PATH = PATH / "Datasets"


def fetch_cal_housing_data(housing_url = DOWNLOAD_ROOT, data_path = DATA_PATH):
    os.makedirs(DATA_PATH, exist_ok = True)
    file_path = DATA_PATH / "cal_housing.tgz"
    urllib.request.urlretrieve(housing_url, file_path)
    housing_tgz = tarfile.open(file_path)
    housing_tgz.extractall(path = data_path)
    housing_tgz.close()
    data = pd.read_csv( data_path / "CaliforniaHousing" / "cal_housing.data", header=None)
    cols = list(pd.read_csv(data_path / "CaliforniaHousing" / "cal_housing.domain", sep = ':',header=None)[0])
    data.columns = cols
    data.to_csv(data_path / "housing_data.csv", index = False)
    print("Done")

def split_test_train(data, test_ratio):
    shuffled = np.random.permutation(len(data))
    test_size = int(len(data)*test_ratio)
    test_indices = shuffled[:test_size]
    train_indices = shuffled[test_size:]
    return data.iloc[train_indices], data.iloc[test_indices]
