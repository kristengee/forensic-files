import requests
from bs4 import BeautifulSoup
import csv
import json

with open("forensic_files.json") as f:
    data = json.load(f)

website_url = requests.get('https://en.wikipedia.org/wiki/Forensic_Files_(season_1)').text

soup = BeautifulSoup(website_url,'html.parser')

My_table = soup.find('table',{'class':'wikitable plainrowheaders'})

titles = My_table.findAll('td',{'class':'summary'})
descriptions = My_table.findAll('td', {'class':'description'})

name = [t.text for t in titles]
desc = [d.text for d in descriptions]


zipped = [list(a) for a in zip(name, desc)]
print(len(zipped))

filename = 'forensicfiles.csv'
fields = ['Title', 'Description']
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerow(zipped)
