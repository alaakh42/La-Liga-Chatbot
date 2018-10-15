 # -*- coding: utf-8 -*-
import re
import urllib
import requests
import wikipedia
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en,ar;q=0.8',
       'Connection': 'keep-alive'
      }

start_url = "https://en.wikipedia.org/wiki/La_Liga?oldformat=true"
base_url = "https://en.wikipedia.org"

try:
    page_response  = requests.get(start_url, headers=hdr)
    if page_response.status_code == 200:
        data = page_response.text
    else:
        print('======== ERROR STATUS NUMBER ======== ', page_response.status_code)
except requests.Timeout as e:
    print("IT IS TIME TO TIMEOUT")
    print(str(e))

soup = BeautifulSoup(data, "html.parser")
# print(soup.prettify())[:100]


first_col = []
teams_links = []
summary = []
history = []
stadiums = []
locations = []
stadiums_capcity = []
table = soup.find("table", style="text-align: left;")
table_body = table.find("tbody")

for row in table_body.find_all("tr")[1:]:
    first_item = row.find_all("td")[0]
    second_item = row.find_all("td")[1]
    third_item = row.find_all("td")[2]
    forth_item = row.find_all("td")[3]
    first_col.append(first_item.text)
    locations.append(second_item.text.strip().replace("\n",""))
    stadiums.append(third_item.text.strip().replace("\n",""))
    stadiums_capcity.append(int(re.sub(r'\[.*?\]', '', forth_item.text.replace(",","")[20:])))

    for link in first_item.find_all("a", href=True):
        print(first_item.text)
        try:
            summary.append(wikipedia.summary(first_item.text, sentences=10))
        except wikipedia.exceptions.DisambiguationError as e:
            print("Error: {0}".format(e))
            summary.append(wikipedia.summary(link['href'].split("/")[2], sentences=10)) #urllib.unquote(link['href'].split("/")[2]).decode('utf8')

        teams_links.append(base_url + link['href'])

        try:
            club_page = requests.get(base_url + link['href'], headers=hdr)
            if club_page.status_code == 200:
                club_page_data = club_page.text
            else:
                print('======== ERROR STATUS NUMBER ======== ', club_page.status_code)
        except requests.Timeout as e:
            print("IT IS TIME TO TIMEOUT")
            print(str(e))

        club_soup = BeautifulSoup(club_page_data, "html.parser")
        # print(first_item.text)
        # print(type(first_item.text))
        print(club_soup.find("h3").text.replace('[edit]',"").replace('\n',''))
        try:
            if wikipedia.WikipediaPage(first_item.text.replace('\n','')).section(u"History") != u'': 
                history.append(wikipedia.WikipediaPage(first_item.text.replace('\n','')).section(u"History"))
            else:
                history.append(wikipedia.WikipediaPage(first_item.text.replace('\n','')).section(club_soup.find("h3").text.replace('[edit]',"").replace('\n','')))
            if wikipedia.WikipediaPage(first_item.text.replace('\n','')).section(club_soup.find("h3").text.replace('[edit]',"").replace('\n','')) == u'':
                history.append(wikipedia.WikipediaPage(urllib.unquote(link['href'].split("/")[2].replace('\n',''))).section(club_soup.find("h3").text.replace('[edit]',"").replace('\n','')))
        except wikipedia.exceptions.DisambiguationError as e:
            print("Error: {0}".format(e))
            if wikipedia.WikipediaPage(urllib.unquote(link['href'].split("/")[2].replace('\n',''))).section(u"History") != u'': 
                history.append(wikipedia.WikipediaPage(urllib.unquote(link['href'].split("/")[2].replace('\n',''))).section(u"History"))
            else:
                history.append(wikipedia.WikipediaPage(urllib.unquote(link['href'].split("/")[2].replace('\n',''))).section(club_soup.find("h3").text.replace('[edit]',"").replace('\n','')))
            

# print(len(first_col))
# print(len(summary))
# print(len(history))

df = pd.DataFrame({'Team': first_col,
     'Summary': summary,
     'History': history,
     'Team_Page': teams_links,
     'Location': locations,
     'Stadium': stadiums,
     'Stadiums_Capcity': stadiums_capcity
    })


df.loc[df['History'].isnull(),'History'] = wikipedia.WikipediaPage(u'FC Barcelona').section(u'1899–1922: Beginnings'),\
                                           wikipedia.WikipediaPage(u'CD Leganés').section(u'History'),\
                                           wikipedia.WikipediaPage(u'Valencia CF').section(u'History')

construct a different variation to the team/ club name
Team_alt = pd.Series(['Deportivo Alaves',
            'Athletic Bilbao',
            'Atletico Madrid' ,
            'Barca',
            'RC Celta de Vigo',
            'SD Eibar',
            'RCD Espanyol',
            'Getafe CF',
            'Girona FC',
            'SD Huesca',
            'Leganes',
            'Levante UD',
            'Rayo Vallecano',
            'Real Betis',
            'Real Madrid CF',
            'Real Sociedad',
            'Sevilla FC',
            'Valencia CF',
            'Real Valladolid',
            'Villarreal CF'])
df['Team_alt'] = Team_alt.values

print(df.head(2))
df.to_csv("data/Teams_data.csv", encoding="utf-8", index=False)
# df.to_csv("data/Teams_data_updates.csv", encoding="utf-8", index=False)