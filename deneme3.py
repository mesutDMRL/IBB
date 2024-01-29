# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 23:31:18 2023

@author: mesut
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
data = pd.read_csv(url+'veriler4.csv')         
grouped = data.groupby('Sensor Adi')
count = grouped.count()

sen = 465
null_list = [0] * sen

start_date = '2023-01-01'
end_date = '2023-12-31'
num_values = sen
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
    'missing_date_list': [0] * sen,
    'bişey': null_list   
}
count = count.assign(**new_columns)

for name, group in grouped:
    start_date = group['Tarih'].min()
    end_date = group['Tarih'].max()
    full_date_range = pd.date_range(start=start_date, end=end_date)
    missing_dates = full_date_range[~full_date_range.isin(group['Tarih'])]
    columns_to_change = ['start_date', 'end_date', 'total_date_number', 'missing_date_number', 'missing_value_rate', 'missing_date_list', 'bişey']
    new_values = [start_date, end_date, len(full_date_range), len(missing_dates), len(missing_dates)/len(full_date_range), list(missing_dates), len(full_date_range)-len(missing_dates)]
    count.loc[name, columns_to_change] = new_values
 
count = count.loc[(count['Tarih'] > 1500) & (count['missing_value_rate'] < 0.1)
                  & (count['missing_date_number'] < 200)]
data = data[data['Sensor Adi'].isin(list(count.index))]
print(count['Tarih'].sum())
# df = pd.read_csv(url+'2021-yl-gunluk-arac-saym.csv', sep = ";", encoding = 'iso8859_9')
# max_counts = df.groupby(['Tarih', 'Sensor Adi'])['Arac Sayisi'].max().reset_index()
# df = df.merge(max_counts, on=['Tarih', 'Sensor Adi', 'Arac Sayisi'], how='inner')
# df = df.drop('Unnamed: 5', axis=1)
# df = df.dropna()
# df['Tarih'] = pd.to_datetime(df['Tarih'])
# df = df.reset_index(drop=True)

# # print(df.info())
# df2 = pd.read_csv(url+'2022-yl-gunluk-arac-saym.csv', sep = ";", encoding = 'utf-8')
# max_counts = df2.groupby(['Tarih', 'Sensor Adi'])['Arac Sayisi'].max().reset_index()
# df2 = df2.merge(max_counts, on=['Tarih', 'Sensor Adi', 'Arac Sayisi'], how='inner')
# df2['Tarih'] = pd.to_datetime(df2['Tarih'])
# df2 = df2.reset_index(drop=True)

# unique21 = df['Sensor Adi'].unique()
# unique22 = df2['Sensor Adi'].unique()
# # unique21X = df['X Koordinati'].unique()
# # unique21Y = df['Y Koordinati'].unique()

# unique21 = np.sort(unique21)
# unique22 = np.sort(unique22)


# orj = pd.read_csv(url+'veriler2.csv')

# unique16 = orj['Sensor Adi'].unique()
# # unique16X = orj['X Koordinati'].unique()
# # unique16Y = orj['Y Koordinati'].unique()
# unique16 = np.sort(unique16)

# ortak_sensorler21 = np.intersect1d(unique16, unique21)
# ortak_sensorler22 = np.intersect1d(unique16, unique22)


# grouped21 = df.groupby('Sensor Adi')
# count21 = grouped21.count()
# grouped22 = df2.groupby('Sensor Adi')
# count22 = grouped22.count()

# # Çizgi grafiği oluşturun
# df = df.sort_values(by='Tarih')
# alemdag=df.loc[df["Sensor Adi"]=="Beylikdüzü"] 

# weekend_dates = alemdag[alemdag['Tarih'].dt.dayofweek.isin([5, 6])]
# plt.figure(figsize=(16, 4))  # Grafiğin boyutunu belirleyebilirsiniz

# plt.plot(alemdag['Tarih'], alemdag['Arac Sayisi'], linestyle='-', color='b', label='Hafta İçi')
# plt.scatter(weekend_dates['Tarih'], weekend_dates['Arac Sayisi'], color='r', label='Hafta Sonu')

# # Eksen etiketlerini ve başlığı ayarlayın
# plt.xlabel('Tarih')
# plt.ylabel('Araç Sayısı')
# plt.title('Araç Sayısı Değişimi')

# # Tarih biçimini ayarlayın (isteğe bağlı)
# plt.xticks(rotation=45)  # Tarih etiketlerini eğik yazdırır

# # Grafiği göster
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()
