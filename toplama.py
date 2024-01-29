# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 23:15:25 2023

@author: mesut
"""

import pandas as pd
import numpy as np
import json


# url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
# df = pd.read_csv(url+"gunluk-arac-saym.csv", sep = ";", encoding = 'iso8859_9')
# df['Tarih'] = pd.to_datetime(df['Tarih'])
# df = df.dropna(subset=['X Koordinati'])

# veri_adet = df["Sensor Adi"].value_counts()
# mask = df['Sensor Adi'].map(veri_adet) > 10
# df = df[mask]
# df=df.loc[(df["Arac Sayisi"]>300)]

url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
df = pd.read_csv(url+"gunluk-arac-saym.csv", sep = ";", encoding = 'iso8859_9')
df = pd.read_csv(url+"veriler7.csv")
df['Tarih'] = pd.to_datetime(df['Tarih'])
df = df.dropna(subset=['X Koordinati'])
df = df.drop(df[df['Sensor Adi'] == 'İsbak Test'].index)

veri_adet = df["Sensor Adi"].value_counts()
mask = df['Sensor Adi'].map(veri_adet) > 10
df = df[mask]
df=df.loc[(df["Arac Sayisi"]>300)]
max_counts = df.groupby(['Tarih', 'Sensor Adi'])['Arac Sayisi'].max().reset_index()
df = df.merge(max_counts, on=['Tarih', 'Sensor Adi', 'Arac Sayisi'], how='inner')
df = df.reset_index(drop=True)


with open(url + "weather_2.json", "r", encoding="utf-8") as file:
    hava_durumu = json.load(file)

hava = pd.DataFrame(hava_durumu)
hava['tarih'] = pd.to_datetime(hava['tarih'])
hava.rename(columns={"tarih" :"Tarih"}, inplace=True)
hava.drop(["sicaklik_gece"], inplace=True, axis=1)

result = pd.merge(df, hava, on="Tarih")
# print(result.info())

with open(url + "resmi_tatiller.json", "r", encoding="utf-8") as file:
    resmi = json.load(file)

ozel_gunler = []
for i in resmi:
    for key, value in i.items():
        fa = (value[0]).split('\n')
    ozel_gunler.extend(fa)   
# ozel_gunler = pd.DataFrame(ozel_gunler, columns=["Tarih"])
# ozel_gunler['Tarih'] = pd.to_datetime(ozel_gunler['Tarih'])

result['resmi_tatiller'] = 0
result.loc[result['Tarih'].isin(ozel_gunler), 'resmi_tatiller'] = 1

with open(url + "hastane.json", "r", encoding="utf-8") as file:
    hastane = json.load(file)
hastane = pd.DataFrame(hastane)
hastane['Sensor Adi'] = hastane['Sensor Adi'].astype(str)
hastane['Sensor Adi'] = hastane['Sensor Adi'].str.replace('[', '').str.replace(']', '')
hastane['Sensor Adi'] = hastane['Sensor Adi'].str.replace("'", "")
hastane.drop(["X Koordinati", "Y Koordinati"], inplace=True, axis=1)

result = pd.merge(result, hastane, on="Sensor Adi")

with open(url + "AVM.json", "r", encoding="utf-8") as file:
    avm = json.load(file)
avm = pd.DataFrame(avm)
avm['Sensor Adi'] = avm['Sensor Adi'].astype(str)
avm['Sensor Adi'] = avm['Sensor Adi'].str.replace('[', '').str.replace(']', '')
avm['Sensor Adi'] = avm['Sensor Adi'].str.replace("'", "")
avm.drop(["X Koordinati", "Y Koordinati"], inplace=True, axis=1)
avm = avm.rename(columns={'Hastane Sayisi': 'AVM Sayisi'})
result = pd.merge(result, avm, on="Sensor Adi")


keys = []
items = []
with open(url + "distance.json", "r", encoding="utf-8") as file:
    distance = json.load(file)
for key in distance:
    for j, k in key.items():
        keys.append(j)
        items.append(k)
items = pd.DataFrame(items)
items['Sensor Adi'] = keys
items['hız'] = items['hız'] * 60
result = pd.merge(result, items, on="Sensor Adi")

result['Tarih'] = pd.to_datetime(result['Tarih']).dt.date
result.drop(["X Koordinati", "Y Koordinati", "nem"], inplace=True, axis=1)
def is_weekday(day):
    if day in ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']:
        return 1
    else:
        return 0
result['gun'] = result['gun'].apply(is_weekday)

def is_rainy(day):
    if 'Yağmur' in day:
        return 1
    elif 'Kar' in day:
        return 2
    else:
        return 0
result['bulut'] = result['bulut'].apply(is_rainy)
result = pd.get_dummies(result, columns=['bulut'])


# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# label = le.fit_transform(result['Sensor Adi'])
# result.drop("Sensor Adi", axis=1, inplace=True)
# result["Sensor Adi"] = label
result.rename(columns={"gun" :"Haftaici"}, inplace=True)
result.rename(columns={"bulut" :"yagmur/kar"}, inplace=True)


result['sicaklik_gunduz'] = result['sicaklik_gunduz'].str.replace('°C', '')
# result['sicaklik_gece'] = result['sicaklik_gece'].str.replace('°C', '')
# result['nem'] = result['nem'].str.replace('%', '')

result['Arac Sayisi'] = result['Arac Sayisi'].astype(float)
result['sicaklik_gunduz'] = result['sicaklik_gunduz'].astype(float)
# result['sicaklik_gece'] = result['sicaklik_gece'].astype(float)
# result['nem'] = result['nem'].astype(float)
# result['resmi_tatilller'] = result['resmi_tatiller'].astype(float)
result['Hastane Sayisi'] = result['Hastane Sayisi'].astype(float)
result['AVM Sayisi'] = result['AVM Sayisi'].astype(float)

result.info()
grouped = result.groupby(['Tarih', 'Sensor Adi'])
filtered = grouped['Arac Sayisi'].idxmax()
result = result.loc[filtered]

grouped = result.groupby('Sensor Adi')
count = grouped.count()
temmuz = grouped.get_group('15 Temmuz Şehitler Köprüsü Yıldız Katılımı')
grouped2 = temmuz.groupby('Tarih')
temmuz2 = grouped2.count()


# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
# result[['Arac Sayisi', 'sicaklik_gunduz', 'sicaklik_gece', 'nem', 'resmi_tatiller', 'Hastane Sayisi', 'AVM Sayisi']] = scaler.fit_transform(result[['Arac Sayisi', 'sicaklik_gunduz', 'sicaklik_gece', 'nem', 'resmi_tatiller', 'Hastane Sayisi', 'AVM Sayisi']])


corrM = result.corr() # koralasyon grafiği
print(result.info())
print(corrM)

# result.to_csv(url+'veriler4.csv', index=False)  # index=False, indeksi CSV dosyasına dahil etmez
