# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 12:06:10 2023

@author: mesut
"""
# İNZVA GUİDE'LARINA SOR
# url = https://forecastegy.com/posts/multivariate-time-series-forecasting-in-python/
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os

path = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/model_deneme/"

data = pd.read_csv(os.path.join(path, 'train.csv'), 
                   parse_dates=['Date'])
features = pd.read_csv(os.path.join(path, 'features.csv'),
                       parse_dates=['Date'])
stores = pd.read_csv(os.path.join(path, 'stores.csv'))

data = pd.merge(data, features, on=['Store', 'Date', 'IsHoliday'], how='left')
data = pd.merge(data, stores, on=['Store'], how='left')

data['Date'] = data['Date'].dt.to_period('W-SAT').dt.start_time

last_date_by_store = data.groupby('Store')['Date'].last()
stores_with_full_data = last_date_by_store[last_date_by_store == data['Date'].max()].index
data = data.loc[data['Store'].isin(stores_with_full_data)]

data['Type_A'] = (data['Type'] == 'A').astype(int)
data['Type_B'] = (data['Type'] == 'B').astype(int)
data['IsHoliday'] = data['IsHoliday'].astype(int)

data['unique_id'] = data['Store'].astype(str) + '_' + data['Dept'].astype(str)
data = data.drop(['MarkDown1', 'MarkDown2', 'MarkDown3', 
                  'MarkDown4', 'MarkDown5', 'Type'], axis=1)
data = data.rename(columns={'Weekly_Sales': 'y', 'Date': 'ds'})
# print(data.info())

train = data.loc[data['ds'] < '2012-01-01']
valid = data.loc[data['ds'] >= '2012-01-01']
h = 4

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor

from window_ops.rolling import rolling_mean, rolling_max, rolling_min
# !pip install window_ops
from mlforecast import MLForecast
# !pip install mlforecast
models = [make_pipeline(SimpleImputer(), 
                        RandomForestRegressor(random_state=0, n_estimators=100)),
          XGBRegressor(random_state=0, n_estimators=100)]


model = MLForecast(models=models,
                   freq='W',
                   lags=[1,2,4],
                   lag_transforms={
                       1: [(rolling_mean, 4), (rolling_min, 4), (rolling_max, 4)], # aplicado a uma janela W a partir do registro Lag
                   },
                   date_features=['week', 'month'],
                   num_threads=6)
dynamic_features = ['IsHoliday', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
static_features = ['Type_A', 'Type_B', 'Size', 'Store', 'Dept']

model.fit(train, id_col='unique_id', time_col='ds', target_col='y', static_features=static_features)

# model.fit(train, id_col='unique_id', time_col='ds', target_col='y', static_features=static_features, max_horizon=h)
p = model.predict(horizon=h, dynamic_dfs=[valid[['unique_id','ds']+dynamic_features]])
p = p.merge(valid[['unique_id', 'ds', 'y']], on=['unique_id', 'ds'], how='left')

def smape(y_true, y_pred):
    return 100 * np.mean(np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred)))
   
print(f"SMAPE Random Forest Pipeline: {smape(p['y'], p['Pipeline'])}\nSMAPE XGBRegressor: {smape(p['y'], p['XGBRegressor'])}")


pd.Series(model.models_['XGBRegressor'].feature_importances_, index=model.ts.features_order_).sort_values(ascending=False).plot.bar(title='Feature Importance XGBRegressor')
