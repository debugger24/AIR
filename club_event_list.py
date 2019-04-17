import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://www.audaxindia.org/events.php')

soup = BeautifulSoup(r.text, 'html.parser')

table_rows = soup.find(id='mytable').tbody.find_all('tr')

event_urls = []

EVENT_URL_PREFIX = 'https://www.audaxindia.org/'

for row in table_rows:
    columns = row.find_all('td')
    club_name = re.findall('<br/>(.+)<!--<br />', str(columns[0]))
    if (len(club_name) > 0):
        events_by_club = row.find_all('a')
        for url in events_by_club:
            event_urls.append(EVENT_URL_PREFIX + url['href'])

# print (event_urls)
for url in event_urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print (soup.find(id="banner").div.find_all(attrs = {"class":"row"})[1].h1.text)
