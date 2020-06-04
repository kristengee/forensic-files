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

imdb_urls = ['https://m.imdb.com/title/tt0247882/episodes/?season=1',
             'https://m.imdb.com/title/tt0247882/episodes/?season=2',
             'https://m.imdb.com/title/tt0247882/episodes/?season=3',
             'https://m.imdb.com/title/tt0247882/episodes/?season=4',
             'https://m.imdb.com/title/tt0247882/episodes/?season=5',
             'https://m.imdb.com/title/tt0247882/episodes/?season=6',
             'https://m.imdb.com/title/tt0247882/episodes/?season=7',
             'https://m.imdb.com/title/tt0247882/episodes/?season=8',
             'https://m.imdb.com/title/tt0247882/episodes/?season=9',
             'https://m.imdb.com/title/tt0247882/episodes/?season=10',
             'https://m.imdb.com/title/tt0247882/episodes/?season=11',
             'https://m.imdb.com/title/tt0247882/episodes/?season=12',
             'https://m.imdb.com/title/tt0247882/episodes/?season=13',
             'https://m.imdb.com/title/tt0247882/episodes/?season=14']

season = []
no_in_season = []
netflix_collection = []
netflix_episode = []
title = []
descriptions = []
ratings = []

for i in range(14):
    website_url = requests.get(urls[i]).text
    imdb_url = requests.get(imdb_urls[i]).text
    soup = BeautifulSoup(website_url, 'html.parser')
    imdb_soup = BeautifulSoup(imdb_url, 'html.parser')

    My_table = soup.find('table', {'class': 'wikitable plainrowheaders'})
    My_ratings = imdb_soup.find('div', {'id': 'eplist'})
    strong_tags = My_ratings.find_all('strong')

    descriptions.extend([d.text for d in My_table.find_all('tr', {'class': 'expand-child'})])
    ratings.extend([r.text for r in strong_tags if r.get('class') is None])

    for row in My_table.find_all('tr', {'class': 'vevent'}):
        cells = row.findAll('td')
        no_in_season.append(cells[0].text)
        season.append(i+1)
        episode_title = cells[1].text[1:-1]
        title.append(episode_title)
        netflix_info = netflix_finder.find_episode(episode_title)
        netflix_collection.append(netflix_info[0])
        netflix_episode.append(netflix_info[1])

zipped = [list(a) for a in zip(season, no_in_season, netflix_collection, netflix_episode, title, descriptions, ratings)]

df = pd.DataFrame(title, columns=['Title'])
df['Episode'] = no_in_season
df['Season'] = season
df['Netflix Collection'] = netflix_collection
df['Netflix Episode'] = netflix_episode
df['Description'] = descriptions
df['Rating'] = ratings
df.to_csv('forensicfiles.csv')

