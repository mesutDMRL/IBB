# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:26:37 2023

@author: mesut
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/model_deneme/4/"

data = pd.read_csv(url+'train.csv', index_col='id', parse_dates=['date'])

data2 = data.loc[(data['store_nbr'] == 1) & (data['family'].isin(['MEATS', 'PERSONAL CARE'])), ['date', 'family', 'sales', 'onpromotion']]


dec25 = list()
for year in range(2013,2017):
    for family in ['MEATS', 'PERSONAL CARE']:
        dec18 = data2.loc[(data2['date'] == f'{year}-12-18') & (data2['family'] == family)]
        dec25 += [{'date': pd.Timestamp(f'{year}-12-25'), 'family': family, 'sales': dec18['sales'].values[0], 'onpromotion': dec18['onpromotion'].values[0]}]
data2 = pd.concat([data2, pd.DataFrame(dec25)], ignore_index=True).sort_values('date')
data2 = data2.rename(columns={'date': 'ds', 'sales': 'y', 'family': 'unique_id'})

grouped = data2.groupby('unique_id')
count = grouped.count()




null_list = [0] * 2

start_date = '2023-01-01'
end_date = '2023-12-31'
num_values = 2

random_dates = pd.to_datetime(np.random.randint(pd.Timestamp(start_date).timestamp(), 
                                                pd.Timestamp(end_date).timestamp(), 
                                                num_values), 
                             unit='s')


new_columns = {
    'start_date': random_dates,
    'end_date': random_dates,
    'total_date_number': null_list,
    'missing_date_number': null_list,   
    'missing_value_rate': null_list,
    'missing_date_list': [0] * 2
    
}
count = count.assign(**new_columns)


for name, group in grouped:
    start_date = group['ds'].min()
    end_date = group['ds'].max()
    full_date_range = pd.date_range(start=start_date, end=end_date)
    missing_dates = full_date_range[~full_date_range.isin(group['ds'])]
    columns_to_change = ['start_date', 'end_date', 'total_date_number', 'missing_date_number', 'missing_value_rate', 'missing_date_list']
    new_values = [start_date, end_date, len(full_date_range), len(missing_dates), len(missing_dates)/len(full_date_range), list(missing_dates)]
    count.loc[name, columns_to_change] = new_values


train = data2.loc[data2['ds'] < '2017-01-01']
valid = data2.loc[(data2['ds'] >= '2017-01-01') & (data2['ds'] < '2017-04-01')]

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

model.fit(train, id_col='unique_id', time_col='ds', target_col='y', static_features=[])

p = model.predict(horizon=90, dynamic_dfs=[valid[['unique_id', 'ds', 'onpromotion']]])
p = p.merge(valid[['unique_id', 'ds', 'y']], on=['unique_id', 'ds'], how='left')

model.preprocess(train, id_col='unique_id', time_col='ds', target_col='y', static_features=[])


model.fit(train, id_col='unique_id', time_col='ds', target_col='y',
            static_features=[], max_horizon=90)

pd.Series(model.models_['RandomForestRegressor'].feature_importances_, index=model.ts.features_order_).sort_values(ascending=False).plot.bar(
            figsize=(1280/96,720/96), title='RandomForestRegressor Feature Importance', xlabel='Features', ylabel='Importance')
