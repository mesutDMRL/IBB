# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 09:04:53 2023

@author: mesut
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from prophet import Prophet


url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
df = pd.read_csv(url+'veriler2.csv')
max_counts = df.groupby(['Tarih', 'Sensor Adi'])['Arac Sayisi'].max().reset_index()
mf = df.merge(max_counts, on=['Tarih', 'Sensor Adi', 'Arac Sayisi'], how='inner')
df = mf.reset_index(drop=True)
temp = df["Sensor Adi"].unique()[:30]
df = df[df['Sensor Adi'].isin(temp)]

# df['Tarih']= pd.to_datetime(df['Tarih']).dt.date
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# label = le.fit_transform(df['Sensor Adi'])
# df.drop("Sensor Adi", axis=1, inplace=True)
# df["Sensor Adi"] = label

# df.rename(columns={"Tarih": "ds", "Arac Sayisi": "y"}, inplace=True)



# sensor = df.loc[df['Sensor Adi'] == 'Atışalanı']
# sensor = sensor.drop(["Sensor Adi", "Hastane Sayisi", "AVM Sayisi", 
#                       "mesafe", "süre", "hız"], axis = 1)

# print(sensor.dtypes)
# sensor.rename(columns={"Tarih": "ds", "Arac Sayisi": "y"}, inplace=True)

# model = Prophet()
# model.fit(df)


# future = list()

# for i in range(12, 22):
#     date = f'2020-12-{i:02d}'
#     future.append([date])

# future = pd.DataFrame(future)
# future.columns = ['ds']
# future['ds']= pd.to_datetime(future['ds'])
# forecast = model.predict(future)

# forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# model.plot(forecast)


import datetime # bir yılı seçip ay bazlı (ay ay) olarak çizdir
dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in df['Tarih']]
# dates.sort()
sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
# df = df.sort_values(by='Tarih')
df['Tarih'] = pd.DataFrame({'Date':sorteddates})
df['Year'], df['Month'],  df['Day'] = df['Tarih'].str.split('-').str
plt.figure(figsize=(20,20))
sns.set_style('whitegrid')
sns.pointplot(x='Arac Sayisi',y='Sensor Adi',data=df, hue='Year',join=False)
# plt.xticks(np.linspace(1,2,5))
# plt.xlabel('Avarage Car Count',{'fontsize' : 'large'})
# plt.ylabel('Sensor',{'fontsize':'large'})
# plt.title("Yearly Average Car Count in Each Sensor",{'fontsize':20})


grouped = df.groupby('Sensor Adi')

count = grouped.count()
temmuz = grouped.get_group('10. Yıl Cad. 2')
start_date = temmuz['Tarih'].min()
end_date = temmuz['Tarih'].max()
full_date_range = pd.date_range(start=start_date, end=end_date)
missing_dates = full_date_range[~full_date_range.isin(temmuz['Tarih'])]
grouped2 = temmuz.groupby('Tarih')
temmuz2 = grouped2.count()

# import datetime
# url2 = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/model_deneme/iki/"
# data = pd.read_csv(url2+'avocado.csv')
# dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in data['Date']]
# dates.sort()
# sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
# data['Date'] = pd.DataFrame({'Date':sorteddates})
# data['Year'], data['Month'],  data['Day'] = data['Date'].str.split('-').str
# plt.figure(figsize=(20,20))
# sns.set_style('whitegrid')
# sns.pointplot(x='AveragePrice',y='region',data=data, hue='year',join=False)
# plt.xticks(np.linspace(1,2,5))
# plt.xlabel('Region',{'fontsize' : 'large'})
# plt.ylabel('Average Price',{'fontsize':'large'})
# plt.title("Yearly Average Price in Each Region",{'fontsize':20})
