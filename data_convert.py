# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:03:21 2023

@author: mesut
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler



url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
df = pd.read_csv(url+'veriler7.csv')
df['Tarih'] = pd.to_datetime(df['Tarih'])
df['Yıl'] = df['Tarih'].dt.year
df['Ay'] = df['Tarih'].dt.month
df['Gün'] = df['Tarih'].dt.day
df2 = df.copy()

encoder = LabelEncoder()
# df['Sensor Adi_2']= encoder.fit_transform(df['Sensor Adi'])



scaler = MinMaxScaler(feature_range=(0, 1))
df[['sicaklik_gunduz', 'Hastane Sayisi', 'AVM Sayisi', 'mesafe', 'süre',
    'hız', 'Yıl', 'Ay', 'Gün']] = scaler.fit_transform(df[[
    'sicaklik_gunduz', 'Hastane Sayisi', 'AVM Sayisi', 'mesafe', 'süre', 
    'hız', 'Yıl', 'Ay', 'Gün']])


df['Sensor_Adi3'] = df['Sensor Adi']

df=df.set_index(['Sensor Adi','Tarih'])
# Because this is panel data so I will split each country_Region's data
def train_test_split(data):
    size=int(len(data)*0.8)
    # for train data will be collected from each country's data which index is from 0-size (80%)
    x_train =data.drop(columns=['Arac Sayisi']).iloc[0:size]
    # for test data will be collected from each country's  data which index is from size to the end (20%)
    x_test = data.drop(columns=['Arac Sayisi']).iloc[size:]
    y_train=data['Arac Sayisi'].iloc[0:size]
    y_test=data['Arac Sayisi'].iloc[size:]
    return x_train, x_test,y_train,y_test

sen=list(set(df['Sensor_Adi3']))
# loop each country_Region and split the data into train and test data
X_train=[]
X_test=[]
Y_train=[]
Y_test=[]
for i in range(0,len(sen)):
    data=df[df['Sensor_Adi3']==sen[i]]
    # applied the function I created above
    x_train, x_test,y_train,y_test=train_test_split(data)
    X_train.append(x_train)
    X_test.append(x_test)
    Y_train.append(y_train)
    Y_test.append(y_test)
    
# concatenate each train dataset in X_train list and Y_train list respectively
X_train=pd.concat(X_train)
Y_train=pd.DataFrame(pd.concat(Y_train))
# concatenate each test dataset in X_test list and Y_test list respectively
X_test=pd.concat(X_test)
Y_test=pd.DataFrame(pd.concat(Y_test))

encoder = LabelEncoder()
#combine X train and Y train as train data
train_data=pd.DataFrame()
train_data[X_train.columns]=X_train
train_data[Y_train.columns]=Y_train
train_data['Sensor_Adi3']= encoder.fit_transform(train_data['Sensor_Adi3'])
#combine X test and Y test as test data
test_data=pd.DataFrame()
test_data[X_test.columns]=X_test
test_data[Y_test.columns]=Y_test
test_data['Sensor_Adi3']= encoder.fit_transform(test_data['Sensor_Adi3'])