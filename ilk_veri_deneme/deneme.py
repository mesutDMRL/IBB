# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 09:36:27 2023

@author: mesut
"""

import pandas as pd
import numpy as np


url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
df = pd.read_csv(url+"hourly_transportation_202001.csv")

sample = df[:10000]

summary = sample.describe()
columns = sample.columns
data_types = sample.dtypes


"""
1) dataframein columları üzerinde gez
2) column typeı obejct olanları filtrele
3) columnların unique valuelarını çıkar
"""

object_columns = [i for i in sample.select_dtypes(include=['object']).columns]
unique_value = [sample[i].unique() for i in object_columns]

int64_values = sample.select_dtypes(include=['int64'])

temp = int64_values.describe()

import matplotlib.pyplot as plt

transition_hour = df.transition_hour.unique()

temp = [(df.transition_hour == i).sum() for i in transition_hour]
temp_2 = [(df.transition_hour == i) for i in transition_hour]
tempreg = pd.DataFrame(temp_2[0])
value_counts = df['transition_hour'].value_counts()

print(value_counts)

#plt.plot(transition_hour,value_counts.sort_index())
#plt.xlabel("saat")
#plt.ylabel("yolcu sayısı")


passanger = [df.loc[df.transition_hour == i]["number_of_passenger"].sum() for i in transition_hour]
passage = [df.loc[df.transition_hour == i]["number_of_passage"].sum() for i in transition_hour]

plt.plot(transition_hour,passanger)
plt.plot(transition_hour,passage)
plt.xlabel("saat")
plt.ylabel("yolcu sayısı")
