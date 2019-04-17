import mysql.connector

sql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="demo@123"
)

## Delete old database
try:
    mysql_cursor = sql_connection.cursor()
    mysql_cursor.execute("DROP DATABASE air")
except:
    print ("Failed to delete air database")

## Create new database
mysql_cursor.execute("CREATE DATABASE air")

## Connect to new database

sql_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="demo@123",
    database="air"
)

mysql_cursor = sql_connection.cursor()

## Create Club table
mysql_cursor.execute('''CREATE TABLE Club (
        clubID INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL
    )''')

## Create Cyclist table
mysql_cursor.execute('''CREATE TABLE Cyclist (
        name VARCHAR(255) NOT NULL,
        air VARCHAR(255) PRIMARY KEY NOT NULL,
        clubID INT NOT NULL,
        FOREIGN KEY (clubID) REFERENCES Club(clubID)
    )''')

## Create Event Table
mysql_cursor.execute('''CREATE TABLE Event (
        eventID INT AUTO_INCREMENT PRIMARY KEY, 
        url VARCHAR(512) UNIQUE NOT NULL,
        distance VARCHAR(32) NOT NULL,
        date DATE NOT NULL,
        clubID INT NOT NULL,
        FOREIGN KEY (clubID) REFERENCES Club(clubID)
    )''')

## Create Event Record Table
mysql_cursor.execute('''CREATE TABLE Record (
        recordID INT AUTO_INCREMENT PRIMARY KEY, 
        air VARCHAR(255) NOT NULL,
        eventID INT NOT NULL,
        time_mins VARCHAR(32) NOT NULL,
        FOREIGN KEY (air) REFERENCES Cyclist(air),
        FOREIGN KEY (eventID) REFERENCES Event(eventID),
        CONSTRAINT air_event UNIQUE (air, eventID)
    )''')


## Show all tables in database
mysql_cursor.execute("SHOW TABLES")

for x in mysql_cursor:
    print(x)



