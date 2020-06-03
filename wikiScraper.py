import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import numpy as np

with open("forensic_files.json") as f:
    data = json.load(f)

website_url = requests.get('https://en.wikipedia.org/wiki/Forensic_Files_(season_1)').text

soup = BeautifulSoup(website_url,'html.parser')

My_table = soup.find('table',{'class':'wikitable plainrowheaders'})

season = []
no_in_season = []
title = []
descriptions = [d.text for d in My_table.find_all('tr', {'class':'expand-child'})]


for row in My_table.find_all('tr', {'class': 'vevent'}):
    cells = row.findAll('td')
    no_in_season.append(cells[0].text)
    season.append(1)
    title.append(cells[1].text)

zipped = [list(a) for a in zip(season, no_in_season, title, descriptions)]

df = pd.DataFrame(title, columns=['Title'])
df['Episode'] = no_in_season
df['Season'] = season
df['Description'] = descriptions
df.to_csv('forensicfiles.csv')