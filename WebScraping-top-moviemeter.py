# sudo pip3 install BeautifulSoup4
print("loading libraries: begin")
import numpy as np
from typing import Text
import pandas as pd
import requests
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from datetime import datetime
print("loading libraries: end")

urls = ("https://www.moviemeter.nl/toplijst/film/1855/top-250-beste-actie-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1846/top-250-beste-komedie-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1861/top-250-beste-oorlog-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1852/top-250-beste-thriller-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1853/top-250-beste-familie-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1854/top-250-beste-animatie-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1859/top-250-beste-avontuur-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1864/top-250-beste-biografie-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1860/top-250-beste-documentaire-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1856/top-250-beste-drama-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1858/top-250-beste-fantasy-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1865/top-50-beste-historisch-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1849/top-250-beste-horror-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1857/top-250-beste-misdaad-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1862/top-250-beste-muziek-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1850/top-250-beste-mystery-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1863/top-50-beste-roadmovie-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1845/top-250-beste-romantiek-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1848/top-250-beste-sciencefiction-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1866/top-50-beste-sport-films-aller-tijden",
        "https://www.moviemeter.nl/toplijst/film/1847/top-50-beste-western-films-aller-tijden")

print("decleare variable: begin")
ds = "global"   # to make this item available outside the script
title = []
alttitle = []
genre = []
rating = []
ratingcount = []
duration = []
print("decleare variable: end")

print("looping sites: begin")
for url in urls:
    # Getting the contents from the each url
    print("getting data from site: " + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Pick a search area
    print("search for an area")
    movies = soup.findAll('tbody')
    # Have a little break between 2 and 10 seconds
    sleep(randint(2,10))

    for item in movies:
        movie = (item.findAll('div', class_='_wrap'))
        for mov in movie:
            count = (len(mov.findAll("div", class_='sub')))
            tmp = (mov.findAll("div", class_='sub'))
            if (tmp):
                ratingcount.append('0')
                title.append(mov.find('a').text)
                if (count == 2):         
                    alttitle.append("")
                    if (tmp[0]):
                        genre.append(tmp[0].text)
                    if (tmp[1]):
                        duration.append(tmp[1].text)
                else:          
                    if (tmp[0]):
                        alttitle.append((tmp[0].text).replace('Alternatieve titel: ',''))
                    if (tmp[1]):
                        genre.append(tmp[1].text)
                    if (tmp[2]):
                        duration.append(tmp[2].text)
            else:
                tmp = mov.findAll("div", class_='mm_star')
                if (tmp):
                    rating.append((tmp[0].text).split('(')[0])
print("looping sites: end")

print("creating dataset: begin")
ds = pd.DataFrame({'title':title,
                       'alttitle':alttitle,
                       'genre':genre,
                       'rating':rating,
                       'duration':duration})
print("creating dataset: end")

print("cleanup: begin")
print("remove duplicates")
before = ds.count().title
ds = ds.drop_duplicates(subset=['title'])
after = ds.count().title
print ("removed duplicates: " + str(before-after))
print("sort by rating")
ds = ds.sort_values('rating', ascending=False)
ds.head()
print("cleanup: end")

print("export: begin")
timestamp = datetime.today().strftime('%Y-%m-%d')
ds.to_csv('top_movies-' + timestamp + '.csv', index=False)
print("export: end")

# Run: python3 WebScraping-top-moviemeter.py
# Run within Python3: exec(open('WebScraping-top-moviemeter.py').read())

# ds: DataSet is now available outside the script, filled with side info
