# AIR

## Medium Article

Medium Article: https://medium.com/@debugger24/brms-in-india-694082dabcfe

## Installation and Execution

1. Install MySQL (https://dev.mysql.com/doc/mysql-installation-excerpt/5.5/en/windows-install-archive.html)

2. Install python 3.7 (https://www.python.org/downloads/release/python-370/)

3. Install following required libraries by executing following command

```
pip install mysql requests bs4 jupyter
```

4. To Initialize Database
```
python init_db.py
```

5. To fetch data
```
python fetch_data.py
```

6. To open jupyter notebook
```
jupyter notebook
```

## Motivation

I love cycling and participating in BRM events since Jan 2019. I saw the AIR website and found good amount of data but it was not summarized the way I wanted, so I started scraping the database and wrote code to summarize the data the way I wanted.

## Files

`init_db.py` --> Contains code to initialize the empty database

`fetch_data.py` --> Contains code to fetch data from AIR website and dump into database

## Analysis

1. Goa Club is conducted most number of events in this year and Bangalore Club had most number of Randonneurs.
2. Most of the Randonneurs participate in BRM 200, followed by 300, 400, 600 BRMs
3. 200, 300 and 400km BRMs have good finishing rate, more than 90% of riders finish it. But 600, 1000 and 1200km BRMs have low finish rate, less than 81%

## Acknowledgement

The data collected is from AIR website (https://audaxindia.org)