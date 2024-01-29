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
from bs4 import BeautifulSoup
import numpy as np
from geopy.distance import great_circle
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

# url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
# df = pd.read_csv(url+"gunluk-arac-saym.csv", sep = ";", encoding = 'iso8859_9')
# df['Tarih'] = pd.to_datetime(df['Tarih'])
# df = df.dropna(subset=['X Koordinati'])

# veri_adet = df["Sensor Adi"].value_counts()
# mask = df['Sensor Adi'].map(veri_adet) > 10
# df = df[mask]
# df=df.loc[(df["Arac Sayisi"]>300)]

tekil.at[206, 'Y Koordinati'] = '40.988017'
tekil.at[206, 'X Koordinati'] = '29.084167'
tekil.at[423, 'Y Koordinati'] = '41.050833'
tekil.at[423, 'X Koordinati'] = '28.885556'
tekil.at[447, 'Y Koordinati'] = '41.06131003100720'
tekil.at[447, 'X Koordinati'] = '28.80686727261250'



X=list(tekil["X Koordinati"][0:1])[0].replace(',', '.')
Y=list(tekil["Y Koordinati"][0:1])[0].replace(',', '.')

API_KEY = "AIzaSyDIfQHLxQmJ0NZkAflxGQy-vXDy6j7IPA0"

map_client = googlemaps.Client(API_KEY)
# YÖN VERİSİNE GÖRE DE HESAPLA  görselleştir bir şekilde verileri grafikler ya 
         # da harita üzerinde falan
mesafeler = {}
mesafe = 0
süre = 0
for i in range(1, len(tekil)):
    Xs=list(tekil["X Koordinati"][i:i+1])[0].replace(',', '.')
    Ys=list(tekil["Y Koordinati"][i:i+1])[0].replace(',', '.')

    try: 
        directions_result = map_client.directions((Y, X), (Ys, Xs), mode="driving")
        KMDistance = (directions_result[0]['legs'][0]['distance']['text'])
        me = float(KMDistance.replace('km', ''))
        mesafe += me
        Duration = (directions_result[0]['legs'][0]['duration']['text'])
        if 'hour' in Duration:
            Duration = Duration.split()
            Duration = str(int(Duration[0])*60 + int(Duration[2]))+' mins'
        sü = float(Duration.replace('mins', ''))
        süre += sü
        baslangic = (directions_result[0]['legs'][0]["start_address"])
        bitis = (directions_result[0]['legs'][0]["end_address"])
        tarif = ""
        for step in directions_result[0]['legs'][0]['steps']:
            tarif  += "\n"+step['html_instructions']
        soup = BeautifulSoup(tarif, 'lxml')
        temiz_metin = soup.get_text()
        adım = len(directions_result[0]['legs'][0]['steps'])
        coords_1 = (Y, X)
        coords_2 = (Ys, Xs)
        distance = great_circle(coords_1, coords_2).kilometers
    except Exception as e:
        KMDistance = None
        Duration = None
        temiz_metin = None
        adım = None
        baslangic = None,
        bitis = None
        print(e, "hatası aldık")
        print(i)
        # print('sensor:', tekil["Sensor Adi"][i:i+1][0])
    mesafeler[i]={
        'mesafe': KMDistance,
        'süre': Duration,
        'yol': temiz_metin,
        'adım':adım,
        'baslangic': baslangic,
        'bitis': bitis,
        'X': Xs,
        'Y': Ys,
        'kus_ucumu':distance
    }
    # break

dfr = pd.DataFrame(mesafeler)
dfr = dfr.transpose()
dfr['mesafe'] = dfr['mesafe'].str.replace('km', '')
dfr['mesafe'] = dfr['mesafe'].str.replace(',', '.')
dfr['mesafe'] = dfr['mesafe'].astype(float)
dfr['kus_ucumu'] = dfr['kus_ucumu'].astype(float)
dfr['süre'] = dfr['süre'].str.replace('mins', '')
dfr['süre'] = dfr['süre'].astype(float)
dfr['adım'] = dfr['adım'].astype(float)

corrM = dfr.corr()

print(corrM)
# print(dfr.dtypes)


# search_string = "AVM"
# distance = 500
# topla = []
# civar_hastane = {}
# sensor = df["Sensor Adi"].unique()
# for i in sensor:
#     hastane_listesi = []
#     print(i)
#     X = list(df.loc[df['Sensor Adi'] == i]['X Koordinati'][0:1])
#     Y = list(df.loc[df['Sensor Adi'] == i]['Y Koordinati'][0:1])
#     Y = Y[0].replace(',', '.')
#     X = X[0].replace(',', '.')
#     try:
#         response = map_client.places_nearby(
#             location = (Y, X),
#             keyword = search_string,
#             name = ['AVM'],
#             radius = distance
#             )
#     except Exception as e:
#         print(e, 'hatası aldık')
#     hastane_listesi.extend(response.get('results'))
#     civar_hastane['Sensor Adi'] = i,
#     civar_hastane['X Koordinati'] = X,
#     civar_hastane['Y Koordinati'] = Y,
#     civar_hastane['Hastane Sayisi'] = len(hastane_listesi)
#     topla.append(civar_hastane)
#     with open(url+"AVM.json", "a", encoding="utf-8") as file:
#         if file.tell() != 0:  # Dosya boş değilse (ilk veri yazılıyor mu?)
#             file.write(",") 
#         json.dump(civar_hastane, file, ensure_ascii=False)
#         file.write("\n")
    
    
    

# hastane_listesi.extend(response.get('results'))

# Distance = map_client.directions((Y, X), (40.988017, 29.084167))


# KMDistance = (Distance[0]['legs'][0]['distance']['text'])
# Duration = (Distance[0]['legs'][0]['duration']['text'])


# tarif = ""
# directions_result = map_client.directions((Y, X), (40.988017, 29.084167), mode="driving")
# for step in directions_result[0]['legs'][0]['steps']:
#     # print(step['html_instructions'])
#     tarif  += "\n"+step['html_instructions']
# soup = BeautifulSoup(tarif, 'lxml')
# temiz_metin = soup.get_text()


    
    
    
