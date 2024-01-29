# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 09:16:47 2023

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

url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
data = pd.read_csv(url+'veriler2.csv')
display(data)
print(f"Shape: {data.shape}")

# Data preprocessing
# ======================================================================================
selected_store = 'Alemdağ'
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