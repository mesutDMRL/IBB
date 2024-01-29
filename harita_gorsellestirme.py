# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 08:58:36 2023

@author: mesut
"""
import pandas as pd
import numpy as np

url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
df = pd.read_csv(url+'gunluk-arac-saym.csv', sep = ";", encoding = 'iso8859_9')
df = df.dropna(subset=['X Koordinati'])
df = df.drop(df[df['Sensor Adi'] == 'İsbak Test'].index)

veri_adet = df["Sensor Adi"].value_counts()
mask = df['Sensor Adi'].map(veri_adet) > 10
df = df[mask]
df=df.loc[(df["Arac Sayisi"]>300)]
max_counts = df.groupby(['Tarih', 'Sensor Adi'])['Arac Sayisi'].max().reset_index()
df = df.merge(max_counts, on=['Tarih', 'Sensor Adi', 'Arac Sayisi'], how='inner')
df = df.reset_index(drop=True)
koordinatlarX = df['X Koordinati'].unique()
koordinatlarY = df['Y Koordinati'].unique()
unique_coords = df[['X Koordinati', 'Y Koordinati']].drop_duplicates()  
unique_coords.at[265415, 'Y Koordinati'] = '41.06131003100720'
unique_coords.at[265415, 'X Koordinati'] = '28.80686727261250'
unique_coords.at[253278, 'Y Koordinati'] = '41.22074014861440'
unique_coords.at[253278, 'X Koordinati'] = '29.00138125995970'
unique_coords.at[148451, 'X Koordinati'] = '28.885556'
unique_coords.at[148451, 'Y Koordinati'] = '41.050833'
unique_coords.at[206, 'X Koordinati'] = '29.084167'
unique_coords.at[206, 'Y Koordinati'] = '40.988017'
unique_coords['X Koordinati'] = unique_coords['X Koordinati'].str.replace(',', '.')
unique_coords['Y Koordinati'] = unique_coords['Y Koordinati'].str.replace(',', '.')


unique_coords = unique_coords.astype(float)
unique_coords = unique_coords.values.tolist()



# !pip install folium
import folium

# İstanbul'ın merkez koordinatları
istanbul_center = [41.0082, 28.9784]

# Folium harita nesnesi oluşturun
m = folium.Map(location=istanbul_center, zoom_start=10)

# İşaretlemek istediğiniz koordinatları ekleyin
coordinates = [[40.9941, 29.0183],[41.0055, 28.9743],[41.0367, 28.9850]]
sample = unique_coords[:10]
for i in unique_coords:
    i.reverse()
# Koordinatları haritaya işaretleyin
for loc in unique_coords:
    folium.Marker(
        location=loc
    ).add_to(m)

# Haritayı görüntüleyin
url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/harita görselleri/"
m.save(url+"istanbul_haritasi5.html")
