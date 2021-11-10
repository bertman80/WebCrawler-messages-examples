# sudo pip3 install BeautifulSoup4
# libraries
import pandas as pd
import requests
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint

ds = "global"   # to make this item available outside the script
url = "https://www.trebnie.nl/artikelen"

# Creating the lists we want to write into
subject = []
time = []
content = []

# Getting the contents from the each url
print("getting data from site: " + url)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# Pick a search area
print("search for an area")
berichtgebied = soup.findAll('div', class_='entry-content')

# Have a little break between 2 and 10 seconds
sleep(randint(2,10))

# Search within the search area for li
for item in berichtgebied:
    li = item.find_all("li")
    print("looking for subitems")
    for line in li:
        subject.append(line.find('a').text)
        time.append(line.find('time', class_='wp-block-latest-posts__post-date').text)
        content.append(line.find('div', class_='wp-block-latest-posts__post-excerpt').text)
        
# create dataset
print("creating dataset")
ds = pd.DataFrame({'subject':subject,
                       'time':time,
                       'content':content})

print(ds.head())

# Run: python3 WebScraping_trebnie.py
# Run within Python3: exec(open('WebScraping_trebnie.py').read())

# ds: DataSet is now available outside the script, filled with side info