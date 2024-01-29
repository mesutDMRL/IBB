# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 09:01:47 2023

@author: mesut
"""


import calendar

def get_year_dates(year):
    year_dates = []

    for month in range(1, 13):  # 1 to 12 represents the months
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            year_dates.append((year, month, day))  # Append the (year, month, day) tuple to the list

    return year_dates

all_dates = []
for i in range(2016, 2024):
    year = i  
    all_dates.append(get_year_dates(i))

# print(all_dates[0][0][0])

from bs4 import BeautifulSoup as bs
import requests 
import datetime
import json


gunler = []
for years in all_dates:
    for days in years:
        days = list(days)   
        # print(type('0'+str(days[1])))
        if len(str(days[1])) < 2:
            # print(days[1], 'ilk')
            days[1] = '0'+str(days[1])
            # print('0'+str(days[1]))
        if len(str(days[2])) < 2:
            days[2] = '0'+str(days[2])
        print(days)
        
        url = f"https://www.havadurumu15gunluk.net/gecmisbilgi/{days[0]}-{days[1]}-{days[2]}-istanbul-havadurumu.html"
        httpRequest = requests.get(url)
        html = httpRequest.text

        parsedHtml = bs(html, "html.parser")
        # print(parsedHtml)

        data = []
        target_row = parsedHtml.find_all('tr')[17]  

        for row in target_row.find_all('td'):
            data.append(row.text)
        # print(data[1].strip())
        try:     
            hava_durumu = {}
            hava_durumu['tarih'] = data[15]
            hava_durumu['gun'] = data[16]
            hava_durumu['sicaklik_gunduz'] = data[19].strip()
            hava_durumu['sicaklik_gece'] = data[20].strip()
            hava_durumu['bulut'] = data[18]
            hava_durumu['nem'] = data[6].strip()
            # print(hava_durumu)
            url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
            with open(url+"weather_2.json", "a", encoding="utf-8") as file:
                if file.tell() != 0:  # Dosya boş değilse (ilk veri yazılıyor mu?)
                    file.write(",") 
                json.dump(hava_durumu, file, ensure_ascii=False)
                file.write("\n")
        except:
            print(url)
            print(days) 
        # break
        gunler.append(hava_durumu)
    # break

# url = "https://www.havadurumu15gunluk.net/gecmisbilgi/2016-02-01-istanbul-havadurumu.html"

# httpRequest = requests.get(url)
# html = httpRequest.text

# parsedHtml = bs(html, "html.parser")
# # print(parsedHtml)

# class_data = parsedHtml.find_all(class_ = 'strong2')
# class_data2 = parsedHtml.find_all(class_ = 'strong3')

# for i, j in zip(class_data, class_data2):
#     print(i.text, j.text)


# data = []

# for row in parsedHtml.find_all('tr'):
#     row_data = []
#     for cell in row.find_all('td'):
#         row_data.append(cell.text)
#     data.append(row_data)
    
# for row in parsedHtml.find_all('tbody'):
#     print(row_data)
#     row_data = []
#     target_row = row.find_all('tr')[0]  
#     for cell in target_row.find_all('td'):
#         row_data.append(cell.text)
#     data.append(row_data)
 
# data = []       
# target_row = parsedHtml.find_all('tr')[17]  

# for row in target_row.find_all('td'):
#     data.append(row.text)
# # print(data[1].strip())

    
# data = []   
# target_row = parsedHtml.find_all('tr')[19]  


# for row in target_row.find_all('td'):
#     data.append(row.text)
# print(data[1].strip())


# for table in parsedHtml.find_all('table'):
#     print(table.get('class'))