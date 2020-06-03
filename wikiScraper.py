import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import netflixFinder

netflix_finder = netflixFinder.NetflixFinder()

urls = ['https://en.wikipedia.org/wiki/Forensic_Files_(season_1)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_2)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_3)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_4)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_5)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_6)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_7)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_8)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_9)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_10)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_11)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_12)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_13)',
        'https://en.wikipedia.org/wiki/Forensic_Files_(season_14)']

season = []
no_in_season = []
netflix_collection = []
netflix_episode = []
title = []
descriptions = []

for i in range(len(urls)):
    website_url = requests.get(urls[i]).text
    soup = BeautifulSoup(website_url, 'html.parser')

    My_table = soup.find('table', {'class': 'wikitable plainrowheaders'})

    descriptions.extend([d.text for d in My_table.find_all('tr', {'class': 'expand-child'})])

    for row in My_table.find_all('tr', {'class': 'vevent'}):
        cells = row.findAll('td')
        no_in_season.append(cells[0].text)
        season.append(i+1)
        episode_title = cells[1].text[1:-1]
        title.append(episode_title)
        netflix_info = netflix_finder.find_episode(episode_title)
        netflix_collection.append(netflix_info[0])
        netflix_episode.append(netflix_info[1])

zipped = [list(a) for a in zip(season, no_in_season, netflix_collection, netflix_episode, title, descriptions)]

df = pd.DataFrame(title, columns=['Title'])
df['Episode'] = no_in_season
df['Season'] = season
df['Netflix Collection'] = netflix_collection
df['Netflix Episode'] = netflix_episode
df['Description'] = descriptions
df.to_csv('forensicfiles.csv')
