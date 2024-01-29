# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 23:01:04 2023

@author: mesut
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 12:59:30 2023

@author: mesut
"""
# BURADAN GÜZEL BİR SINIF ÇIKAR. BİR SINIF YAZ
# !pip install googlemaps
#adım verisi ile mesafe verisi arasındaki korelasyonu analiz et. süre verisini de analiz et
# yön bilgisi bulmaya çalış
import googlemaps
import pandas as pd
import numpy as np
import json


url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
df = pd.read_csv(url+"gunluk-arac-saym.csv", sep = ";", encoding = 'iso8859_9')
df2 = df.dropna(subset=['X Koordinati'])
unique_counts = df2['Sensor Adi'].value_counts()
mask = df2['Sensor Adi'].map(unique_counts) > 10
df = df2[mask]
df = df.drop(df[df['Sensor Adi'] == 'İsbak Test'].index)


yinelenen_satirlar = df[df.duplicated(subset='Sensor Adi')]
tekil = df.drop(yinelenen_satirlar.index)
tekil = tekil.dropna(subset=['X Koordinati'])
tekil=tekil.loc[(tekil["Arac Sayisi"]>300)]
print(len(tekil))
tekil = tekil.reset_index(drop=True)

tekil.at[206, 'Y Koordinati'] = '40.988017'
tekil.at[206, 'X Koordinati'] = '29.084167'
tekil.at[423, 'Y Koordinati'] = '41.050833'
tekil.at[423, 'X Koordinati'] = '28.885556'
tekil.at[447, 'Y Koordinati'] = '41.06131003100720'
tekil.at[447, 'X Koordinati'] = '28.80686727261250'

API_KEY = "AIzaSyDIfQHLxQmJ0NZkAflxGQy-vXDy6j7IPA0"

map_client = googlemaps.Client(API_KEY)

def ustfonk(tekil):
    for i in tekil.index:
        print(i)
        X=list(tekil["X Koordinati"][i:i+1])[0].replace(',', '.')
        Y=list(tekil["Y Koordinati"][i:i+1])[0].replace(',', '.')
        SensorAdi = tekil["Sensor Adi"][i]
        df = tekil.drop(i)
        df = df.reset_index(drop=True)
        mesafefonk(df, Y, X, SensorAdi)

def mesafefonk(df, Y, X, SensorAdi):
    mesafeler = {}
    mesafe = 0
    süre = 0
    for i in range(0, len(df)):
        Xs=list(tekil["X Koordinati"][i:i+1])[0].replace(',', '.')
        Ys=list(tekil["Y Koordinati"][i:i+1])[0].replace(',', '.')
        try: # YÖN VERİSİNE GÖRE DE HESAPLA  görselleştir bir şekilde verileri grafikler
             # ya da harita üzerinde falan
            directions_result = map_client.directions((Y, X), (Ys, Xs), mode="driving")
            KMDistance = (directions_result[0]['legs'][0]['distance']['text'])
            if ' m' in KMDistance:
                KMDistance = str(float(KMDistance.replace('m', ''))*0.001)
            me = float(KMDistance.replace('km', ''))
            mesafe += me
            Duration = (directions_result[0]['legs'][0]['duration']['text'])
            if 'hour' in Duration:
                Duration = Duration.split()
                Duration = str(int(Duration[0])*60 + int(Duration[2]))+' mins'
            sü = float(Duration.replace('mins', '').replace('min', ''))
            süre += sü
        except Exception as e:
            KMDistance = None
            Duration = None
            print(e, "hatası aldık")
    mesafeler[SensorAdi]={
        'mesafe': mesafe/len(df),
        'süre': süre/len(df),
        'hız': mesafe/süre
    }
    with open(url+"distance.json", "a", encoding="utf-8") as file:
        if file.tell() != 0:  # Dosya boş değilse (ilk veri yazılıyor mu?)
            file.write(",") 
        json.dump(mesafeler, file, ensure_ascii=False)
        file.write("\n")
    


ustfonk(tekil)
