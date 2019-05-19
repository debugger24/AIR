import mysql.connector
import requests
from bs4 import BeautifulSoup
import re
import datetime

sql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="demo@123",
    database="air"
)

mysql_cursor = sql_connection.cursor()

def get_club_id(club_name):
    '''
        args:
            club_name: string
        return:
            clubID or None
    '''
    query = 'SELECT * FROM Club WHERE name = %s'
    value = (club_name, )
    mysql_cursor.execute(query, value)
    result = mysql_cursor.fetchall()
    if (len(result) == 1):
        return result[0][0]
    else:
        return None

def insert_clubs(club_names):
    '''
        args:
            club_names: list
    '''
    if (len(club_names) > 0):
        club_names_tuple = []
        for club_name in club_names:
            club_names_tuple.append((club_name, ))
        query = 'INSERT INTO Club (name) VALUES (%s)'
        values = club_names_tuple
        mysql_cursor.executemany(query, values)
        sql_connection.commit()
        print (mysql_cursor.rowcount, "Clubs Inserted")
    else:
        print (0, "Clubs Inserted")

def get_event_id(eventURL):
    query = 'SELECT * FROM Event WHERE url = %s'
    value = (eventURL, )
    mysql_cursor.execute(query, value)
    result = mysql_cursor.fetchall()
    if (len(result) == 1):
        return result[0][0]
    else:
        return None

def insert_event(eventURL, distance, date, club_name):
    clubID = get_club_id(club_name)
    query = 'INSERT INTO Event (url, distance, date, clubID) VALUES (%s, %s, %s, %s)'
    value = (eventURL, distance, date, clubID)
    mysql_cursor.execute(query, value)
    sql_connection.commit()

def insert_cyclist(cyclists):
    if (len(cyclists) > 0):
        query = 'INSERT INTO Cyclist (name, air, clubID) VALUES (%s, %s, %s)'
        values = cyclists
        mysql_cursor.executemany(query, values)
        sql_connection.commit()
        print (mysql_cursor.rowcount, "Cyclist Inserted")
    else:
        print (0, "Cyclist Inserted")

def insert_record(records):
    query = 'INSERT INTO Record (air, eventID, time_mins) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE time_mins = VALUES (time_mins);'
    values = records
    mysql_cursor.executemany(query, values)
    sql_connection.commit()
    print (mysql_cursor.rowcount, "Records Inserted/Updated")

def get_all_clubs():
    query = 'SELECT * FROM Club'
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    return result

def get_all_cyclists():
    query = 'SELECT * FROM Cyclist'
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    return result

def get_all_records():
    query = 'SELECT * FROM Record'
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    return result


## Insert Record

## Fetch records
def fetch_records(eventURL):
    r = requests.get(eventURL)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = []
    for record_soup in soup.find(id="fellowriders").table.tbody.find_all('tr'):
        record = {}
        record['name'] = record_soup.find_all('td')[1].text.strip()
        record['air_number'] = record_soup.find_all('td')[2].text.strip()
        time = record_soup.find_all('td')[5].text.strip()
        if(re.search('.+h.+m', time)):
            hrs = re.findall('(.+)h', time)
            mins = re.findall(' (.+)m', time)
            record['time'] = int(hrs[0]) * 60 + int(mins[0])
        else:
            record['time'] = time
        record['club'] = record_soup.find_all('td')[6].text.strip().title()
        data.append(record)
    return data

def insert_new_clubs_in_db(data):
    clubs = get_all_clubs()
    old_clubs = []
    for club in clubs:
        old_clubs.append(club[1])
    new_clubs = []
    for record in data:
        if record['club'] not in old_clubs:
            if record['club'] not in new_clubs:
                new_clubs.append(record['club'])
    insert_clubs(new_clubs)

def insert_new_cyclist_in_db(data):
    clubs = get_all_clubs()
    clubs_dict = {}
    for club in clubs:
        clubs_dict[club[1]] = club[0]
    cyclists = get_all_cyclists()
    old_air = []
    for cyclist in cyclists:
        old_air.append(cyclist[1])
    new_cyclist_air = []
    new_cyclist = []
    for record in data:
        if record['air_number'] not in old_air:
            if record['air_number'] not in new_cyclist_air:
                new_cyclist.append((record['name'], record['air_number'], clubs_dict[record['club']]))
                new_cyclist_air.append(record['air_number'])
    insert_cyclist(new_cyclist)

def insert_new_record_in_db(data, eventURL):
    ## Drop all records with current eventURL
    clubs = get_all_clubs()
    clubs_dict = {}
    for club in clubs:
        clubs_dict[club[1]] = club[0]
    eventID = get_event_id(eventURL)
    records = []
    for record in data:
        records.append((record['air_number'], eventID, record['time']))
    insert_record(records)

def get_event_details(eventURL):
    r = requests.get(eventURL)
    soup = BeautifulSoup(r.text, 'html.parser')
    club_name = soup.find(id="banner").div.find_all(attrs = {"class":"row"})[0].h2.text.strip()
    distance = re.findall('(.+) BRM', soup.find(id="banner").div.find_all(attrs = {"class":"row"})[1].h1.text)[0].strip()
    date_string = re.findall('on (.+)', soup.find(id="banner").div.find_all(attrs = {"class":"row"})[1].h1.text)[0].strip()
    date_object = datetime.datetime.strptime(date_string, '%d-%b-%Y')
    date = str(date_object.year) + '-' + str(date_object.month) + '-' + str(date_object.day)
    return club_name, distance, eventURL, date

eventURL = 'https://www.audaxindia.org/event-e-2352'
OVERWRITE_EVENT = True

def fetch_and_dump(eventURLs):
    for i, eventURL in enumerate(eventURLs):

        if (OVERWRITE_EVENT == False):
            if (get_event_id(eventURL)):
                print ("\n\nProcessing ", i+1, "/", len(eventURLs) ,"\t", "Skipping\t", eventURL)
                continue

        club_name, distance, eventURL, date = get_event_details(eventURL)

        print ("\n\nProcessing ", i+1, "/", len(eventURLs) ,"\t", club_name, "\t", distance, "\t", eventURL, "\t", date)

        if (not get_club_id(club_name.title())):
            insert_clubs([club_name.title()])

        data = fetch_records(eventURL)

        ## Insert New Clubs in Database
        insert_new_clubs_in_db(data)

        ## Insert New Cyclist in Database
        insert_new_cyclist_in_db(data)

        ## Insert Event in Database
        if (not get_event_id(eventURL)):
            insert_event(eventURL, distance, date, club_name)

        ## Insert Record in Database
        insert_new_record_in_db(data, eventURL)

def get_event_urls():
    '''
        args:
            
        return:
            List of event URLs on event page
    '''
    URL_PREFIX = "https://www.audaxindia.org/"
    EVENT_PAGE_URL = "https://www.audaxindia.org/events.php"
    events_links = []
    r = requests.get(EVENT_PAGE_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    event_tags = soup.find(id='mytable').tbody.find_all('a')
    for event_tag in event_tags:
        events_links.append(URL_PREFIX + event_tag['href'])
    print ("\n\nFound", len(events_links), "URLs on page", EVENT_PAGE_URL, "\n\n")
    return events_links

event_urls = get_event_urls()
fetch_and_dump(event_urls)
