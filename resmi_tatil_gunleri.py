# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 10:02:38 2023

@author: mesut
"""
import json
url = "C:/Users/mesut/OneDrive/Masaüstü/python/IBB/"
ikibinOnaltı = """01 01 2016 
23 04 2016 
01 05 2016 
19 05 2016 
04 07 2016
05 07 2016
06 07 2016
07 07 2016
30 08 2016
11 09 2016
12 09 2016
13 09 2016
14 09 2016
15 09 2016
28 10 2016
29 10 2016"""
resmi = {}
resmi[2016] = ikibinOnaltı.split("|n")
with open(url+"resmi_tatiller.json", "a", encoding="utf-8") as file:
                json.dump(resmi, file, ensure_ascii=False)
ikibinOnyedi = """01 01 2017
23 04 2017
01 05 2017 
19 05 2017 
24 06 2017
25 06 2017
26 06 2017
27 06 2017
30 08 2017
31 08 2017
01 09 2017
02 09 2017
03 09 2017
04 09 2017
28 10 2017
29 10 2017"""
resmi = {}
resmi[2017] = ikibinOnyedi.split("|n")
with open(url+"resmi_tatiller.json", "a", encoding="utf-8") as file:
                json.dump(resmi, file, ensure_ascii=False)
ikibinOnsekiz = """01 01 2018
23 04 2018
01 05 2018 
19 05 2018 
14 06 2018
15 06 2018
16 06 2018
17 06 2018
20 08 2018
21 08 2018
22 08 2018
23 08 2018
24 08 2018
30 08 2018
28 10 2018
29 10 2018"""
resmi = {}
resmi[2018] = ikibinOnsekiz.split("|n")
with open(url+"resmi_tatiller.json", "a", encoding="utf-8") as file:
                json.dump(resmi, file, ensure_ascii=False)
ikibinOndokuz = """01 01 2019
23 04 2019
01 05 2019 
19 05 2019 
04 06 2019
05 06 2019
06 06 2019
07 06 2019
10 08 2019
11 08 2019
12 08 2019
13 08 2019
14 08 2019
30 08 2019
28 10 2019
29 10 2019"""
resmi = {}
resmi[2019] = ikibinOndokuz.split("|n")
with open(url+"resmi_tatiller.json", "a", encoding="utf-8") as file:
                json.dump(resmi, file, ensure_ascii=False)
ikibinYirmi = """01 01 2020
23 04 2020
01 05 2020 
19 05 2020 
23 05 2020
24 05 2020
25 05 2020
26 05 2020
30 07 2020
31 07 2020
01 08 2020
02 08 2020
03 08 2020
30 08 2020
28 10 2020
29 10 2020"""
resmi = {}
resmi[2020] = ikibinYirmi.split("|n")
with open(url+"resmi_tatiller.json", "a", encoding="utf-8") as file:
                json.dump(resmi, file, ensure_ascii=False)
ikibinYirmibir = """01 01 2021
23 04 2021
01 05 2021 
12 05 2021 
13 05 2021
14 05 2021
15 05 2021
19 05 2021
19 07 2021
20 07 2021
21 07 2021
22 07 2021
23 07 2021
31 08 2021
28 10 2021
29 10 2021"""
resmi = {}
resmi[2021] = ikibinYirmibir.split("|n")
with open(url+"resmi_tatiller.json", "a", encoding="utf-8") as file:
                json.dump(resmi, file, ensure_ascii=False)
ikibinYirmiiki = """01 01 2022
23 04 2022
01 05 2022 
01 05 2022 
02 05 2022
03 05 2022
04 05 2022
19 05 2022
08 07 2022
09 07 2022
10 07 2022
11 07 2022
12 07 2022
30 08 2022
28 10 2022
29 10 2022"""
resmi = {}
resmi[2022] = ikibinYirmiiki.split("|n")
with open(url+"resmi_tatiller.json", "a", encoding="utf-8") as file:
                json.dump(resmi, file, ensure_ascii=False)
ikibinYirmiuc = """01 01 2023
23 04 2023
20 04 2023 
21 04 2023 
22 04 2023
23 04 2023
01 05 2023
19 05 2023
27 06 2023
28 06 2023
29 06 2023
30 06 2023
01 07 2023
30 08 2023
28 10 2023
29 10 2023"""
resmi = {}
resmi[2023] = ikibinYirmiuc.split("|n")
with open(url+"resmi_tatiller.json", "a", encoding="utf-8") as file:
                json.dump(resmi, file, ensure_ascii=False)

