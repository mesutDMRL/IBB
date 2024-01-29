# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 09:45:12 2023

@author: mesut
"""

# TIME SERIES PROBLEMS

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
data = pd.read_csv(url+'veriler4.csv', parse_dates=['Tarih'])
temp = data["Sensor Adi"].unique()[8:10]
data = data[data['Sensor Adi'].isin(temp)]  
data.reset_index(drop=True, inplace=True)
# grouped = data.groupby('Sensor Adi')
# count = grouped.count()
# temmuz = grouped.get_group('15 Temmuz Şehitler Köprüsü Yıldız Katılımı')
# grouped2 = temmuz.groupby('Tarih')
# temmuz2 = grouped2.count()
data = data.rename(columns={'Tarih':'ds', 'Arac Sayisi':'y',
                            'Sensor Adi': 'unique_id'})
# data = data[['ds', 'y', 'unique_id']]
train = data.loc[data['ds'] < '2020-01-01']
valid = data.loc[(data['ds'] >= '2020-01-01')]
grouped = valid.groupby(['ds', 'unique_id'])



# null_list = [0] * 10

# start_date = '2023-01-01'
# end_date = '2023-12-31'
# num_values = 10

# random_dates = pd.to_datetime(np.random.randint(pd.Timestamp(start_date).timestamp(), 
#                                                 pd.Timestamp(end_date).timestamp(), 
#                                                 num_values), 
#                               unit='s')


# new_columns = {
#     'start_date': random_dates,
#     'end_date': random_dates,
#     'total_date_number': null_list,
#     'missing_date_number': null_list,   
#     'missing_value_rate': null_list,
#     'missing_date_list': [0] * 10,
#     'bişey': null_list
    
# }
# count = count.assign(**new_columns)


# for name, group in grouped:
#     start_date = group['Tarih'].min()
#     end_date = group['Tarih'].max()
#     full_date_range = pd.date_range(start=start_date, end=end_date)
#     missing_dates = full_date_range[~full_date_range.isin(group['Tarih'])]
#     columns_to_change = ['start_date', 'end_date', 'total_date_number', 'missing_date_number', 'missing_value_rate', 'missing_date_list', 'bişey']
#     new_values = [start_date, end_date, len(full_date_range), len(missing_dates), len(missing_dates)/len(full_date_range), list(missing_dates), len(full_date_range)-len(missing_dates)]
#     count.loc[name, columns_to_change] = new_values
 

from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor

models = [RandomForestRegressor(random_state=0, n_estimators=100),
          ExtraTreesRegressor(random_state=0, n_estimators=100)]

from numba import njit

@njit
def diff(x, lag):
    x2 = np.full_like(x, np.nan)
    for i in range(lag, len(x)):
        x2[i] = x[i] - x[i-lag]
    return x2

# !pip install window_ops
from window_ops.rolling import rolling_mean
from mlforecast import MLForecast

model = MLForecast(models=models,
                   freq='D',
                   lags=[1,7,14],
                   lag_transforms={
                       1: [(rolling_mean, 3), (rolling_mean, 7), (rolling_mean, 28), (diff, 1), (diff, 7)],
                   },
                   date_features=['dayofweek'],
                   num_threads=6)

static_features = ['Hastane Sayisi', 'AVM Sayisi', 'mesafe', 'süre', 'hız']
model.fit(train, id_col='unique_id', time_col='ds', target_col='y',
          static_features=static_features)
dynamic_features = ['unique_id', 'ds', 'Haftaici', 'sicaklik_gunduz',
                             'resmi_tatiller', 'bulut_0', 'bulut_1', 'bulut_2']
p = model.predict(h=90, dynamic_dfs=[valid[['unique_id','ds']+dynamic_features]])
p = p.merge(valid[['unique_id', 'ds', 'y']], on=['unique_id', 'ds'], how='left')

model.fit(train, id_col='unique_id', time_col='ds', target_col='y',
            static_features=[], max_horizon=90)

pd.Series(model.models_['RandomForestRegressor'].feature_importances_, index=model.ts.features_order_).sort_values(ascending=False).plot.bar(
            figsize=(1280/96,720/96), title='RandomForestRegressor Feature Importance', xlabel='Features', ylabel='Importance')


