# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 13:41:27 2023

@author: mesut
"""

import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-darkgrid')
from statsmodels.graphics.tsaplots import plot_acf

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import  HistGradientBoostingRegressor
from lightgbm import LGBMRegressor

# !pip install skforecast
from skforecast.ForecasterAutoregMultiSeries import ForecasterAutoregMultiSeries
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.model_selection import backtesting_forecaster
from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection_multiseries import backtesting_forecaster_multiseries
from skforecast.model_selection_multiseries import grid_search_forecaster_multiseries

url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/model_deneme/3/"
data = pd.read_csv(url+'train.csv')
display(data)
print(f"Shape: {data.shape}")

# Data preprocessing
# ======================================================================================
selected_store = 2
selected_items = data.item.unique() # All items
#selected_items = [1, 2, 3, 4, 5] # Selection of items to reduce computation time

data = data[(data['store'] == selected_store) & (data['item'].isin(selected_items))].copy()
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
data = pd.pivot_table(
           data    = data,
           values  = 'sales',
           index   = 'date',
           columns = 'item'
       )
data.columns.name = None
data.columns = [f"item_{col}" for col in data.columns]
data = data.asfreq('1D')
data = data.sort_index()
data.head(4)

# Split data into train-validation-test
# ======================================================================================
end_train = '2016-05-31 23:59:00'
end_val = '2017-05-31 23:59:00'

data_train = data.loc[:end_train, :].copy()
data_val   = data.loc[end_train:end_val, :].copy()
data_test  = data.loc[end_val:, :].copy()

print(f"Train dates      : {data_train.index.min()} --- {data_train.index.max()}  (n={len(data_train)})")
print(f"Validation dates : {data_val.index.min()} --- {data_val.index.max()}  (n={len(data_val)})")
print(f"Test dates       : {data_test.index.min()} --- {data_test.index.max()}  (n={len(data_test)})")


# Plot time series
# ======================================================================================
fig, ax = plt.subplots(figsize=(8, 5))
data.iloc[:, :4].plot(
    legend   = True,
    subplots = True, 
    sharex   = True,
    title    = 'Sales of store 2',
    ax       = ax, 
)
fig.tight_layout();

# Autocorrelation plot
# ======================================================================================
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(8, 5), sharex=True)
axes = axes.flat
for i, col in enumerate(data.columns[:4]):
    plot_acf(data[col], ax=axes[i], lags=7*5)
    axes[i].set_ylim(-1, 1.1)
    axes[i].set_title(f'{col}')
fig.tight_layout()
plt.show()