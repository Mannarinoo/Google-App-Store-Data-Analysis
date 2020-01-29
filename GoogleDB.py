# Author: Joey Mannarino and Giovanni Grecco
# Milestone 2 Assignment
# 11/3/2019
import csv

import pandas as pd
import pymysql


# Connecting to the AWS database using the host and correct credentials

def make_connection():
    return pymysql.connect(host='productsdb.cneslim7ztlh.us-east-1.rds.amazonaws.com', user='admin', passwd='password',
                           port=3306, autocommit=True)


# making a open connection
cnx = make_connection()

# creating a cursor to execute statements
cur = cnx.cursor()


# Using the cursor to execute SQL statements and create the database
def create_database():
    cur.execute('DROP DATABASE IF EXISTS GoogleAppDB');
    cur.execute('CREATE DATABASE GoogleAppDB');
    cur.execute('USE GoogleAppDB');
    cur.execute('DROP TABLE IF EXISTS Apps');
    cur.execute('DROP TABLE IF EXISTS Genre');
    cur.execute('DROP TABLE IF EXISTS Category');


# Using the cursor to execute SQL statements and create the tables
def create_categorytable():
    cur.execute('USE GoogleAppDB');
    cur.execute('''CREATE TABLE Category (
   CategoryID Integer AUTO_INCREMENT NOT NULL,
   Category varchar(30) NOT NULL,
   PRIMARY KEY (CategoryID)
 )   ''');


def create_genrestable():
    cur.execute('USE GoogleAppDB');
    cur.execute('''CREATE TABLE Genres (
   GenreID Integer Auto_Increment Not Null,
   Genre varchar(30) NOT NULL,
   PRIMARY KEY (GenreID)
 )   ''');


def create_appstable():
    cur.execute('USE GoogleAppDB');
    cur.execute('''CREATE TABLE Apps (
   AppID Integer AUTO_INCREMENT NOT NULL,
   CategoryID Integer NOT NULL,
   Name varchar(50) NOT NULL,
   Rating varchar(20),
   Reviews INT,
   Size varchar(20),
   Type varchar(30),
   Installs varchar(20),
   Price varchar(20),
   CurrentVer varchar(20),
   ContentRating varchar(30),
   PRIMARY KEY (AppID),
   FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
)   ''');


def create_genreappstable():
    cur.execute('USE GoogleAppDB');
    cur.execute('''CREATE TABLE GenreApp (
  GenreID Integer NOT NULL,
  AppID Integer NOT NULL,
  PRIMARY KEY (GenreID, AppID),
  FOREIGN KEY (GenreID) REFERENCES Genres(GenreID),
  FOREIGN KEY (AppID) REFERENCES Apps(AppID)
)   ''');


def insert_data():
    # Opening and reading the file with the data and putting it into a dataframe
    iris = pd.read_csv('GoogleData.csv',
                       names=['Name', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type', 'Price',
                              'Content Rating', 'Genres', 'Last Updated', 'Current Ver', 'Andriod Ver'])
    Appname = iris['Name']
    Category = iris['Category']
    Rating = iris['Rating']
    Reviews = iris['Reviews']
    Size = iris['Size']
    Installs = iris['Installs']
    Type = iris['Type']
    Price = iris['Price']
    ContentRating = iris['Content Rating']
    Genres = iris['Genres']
    LastUpdated = iris['Last Updated']
    CurrentVer = iris['Current Ver']
    AndriodVer = iris['Andriod Ver']

    for count in range(0, len(iris.index)):

        cur.execute('USE GoogleAppDB');
        cur.execute('SELECT count(Category) FROM Category WHERE Category = %s ', (Category[count]))

        if cur.fetchone()[0] == 0:
            cur.execute('''INSERT IGNORE INTO Category (Category) VALUES ( %s )''', (Category[count]))
            cur.execute('SELECT CategoryID FROM Category WHERE Category = %s ', (Category[count]))
            ThecategoryID = int(cur.fetchone()[0])

        cur.execute('SELECT Category FROM Category WHERE Category = %s ', (Category[count]))
        if cur.fetchone()[0] is None:
            cur.execute('''INSERT IGNORE INTO Category (Category) VALUES ( %s )''', (Category[count]))

        cur.execute('SELECT CategoryID FROM Category WHERE Category = %s ', (Category[count]))
        ThecategoryID = int(cur.fetchone()[0])

        try:
         cur.execute('''INSERT IGNORE INTO Apps (CategoryID, Name, Rating, Reviews,  Size, Type, Installs, Price, CurrentVer, ContentRating) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s )''',(ThecategoryID, Appname[count], float(Rating[count]), Reviews[count], Size[count], Type[count],Installs[count], Price[count], CurrentVer[count], ContentRating[count]))
         cur.execute('SELECT AppID FROM Apps WHERE Name = %s ', (Appname[count]))
         TheappID = cur.fetchone()[0]
        except:
         pass
        if count > 0:

            cur.execute('SELECT GenreID FROM Genres WHERE Genre = %s ', (Genres[count]))
            GenreID = cur.fetchone()
            if GenreID is None:
                cur.execute('''INSERT IGNORE INTO Genres (Genre) VALUES ( %s )''', (Genres[count]))
        else:
            cur.execute('''INSERT IGNORE INTO Genres (Genre) VALUES ( %s )''', (Genres[count]))
        try:
         cur.execute('SELECT GenreID FROM Genres WHERE Genre = %s ', (Genres[count]))
         GenreID = cur.fetchone()
         cur.execute('''INSERT INTO GenreApp(GenreID, AppID) VALUES ( %s, %s )''', (GenreID, TheappID))
        except:
         pass

create_database()
create_categorytable()
create_appstable()
create_genrestable()
create_genreappstable()
insert_data()

cur.close();
cnx.commit();
cnx.close();
