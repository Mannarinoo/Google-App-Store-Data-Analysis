import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import numpy as np
import matplotlib.ticker as ticker

def make_connection():
    return pymysql.connect(host='database.c24by8ob2wiy.us-east-1.rds.amazonaws.com', user='admin', passwd='password',
                           port=3306, autocommit=True)


# making a open connection
cnx = make_connection()

# creating a cursor to execute statements
cur = cnx.cursor()



def reviews_bargraph():

    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT a.name
        FROM Apps a
        GROUP BY a.name
        ORDER BY Reviews DESC
        LIMIT 5 ''');
    result = cur.fetchall()
    names = [item for t in result for item in t]
    print(names)

    cur.execute('''SELECT a.Reviews
        FROM Apps a
        GROUP BY a.name
        ORDER BY Reviews DESC
        LIMIT 5 ''');
    result = cur.fetchall()
    reviews = [item for t in result for item in t]
    print(reviews)


    y_pos = np.arange(len(names))

    # Create bars and choose color
    fig = plt.bar(y_pos, reviews, color=('#ffa500'))

    # Add title and axis names
    plt.title('Most Reviewed Apps')
    plt.xlabel('Apps')
    plt.ylabel('Reviews (10 Milion)')
    # Limits for the Y axis
    plt.ylim(4000000, 85000000)
    # Create names
    plt.xticks(y_pos, names)
    plt.xticks(fontsize=8, rotation=90)
    # Show graphic
    plt.show()



def Category_piechart():
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT c.Category
        FROM Apps a, Category c
        WHERE a.CategoryID = c.CategoryID
        GROUP BY c.Category
        ORDER BY COUNT(a.name) DESC
        LIMIT 5 ''');
    result = cur.fetchall()
    Categories = [item for t in result for item in t]
    print(Categories)

    cur.execute('''SELECT COUNT(a.name) as TotalApps
        FROM Apps a, Category c
        WHERE a.CategoryID = c.CategoryID
        GROUP BY c.Category
        ORDER BY COUNT(a.name) DESC
        LIMIT 5 ''');
    result = cur.fetchall()
    Totals = [item for t in result for item in t]
    print(Totals)

    labels = Categories
    sizes = [15, 30, 45, 10]
    explode = (0.1, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(Totals, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Percentage of Apps in Each Category")
    plt.show()

def contentrating_piechart():
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT a.ContentRating
        FROM Apps a
        GROUP BY a.ContentRating
        ORDER BY COUNT(a.name) DESC
        LIMIT 4''');
    result = cur.fetchall()
    ContentRating = [item for t in result for item in t]
    print(ContentRating)

    cur.execute('''SELECT COUNT(a.name) as TotalApps
        FROM Apps a
        GROUP BY a.ContentRating
        ORDER BY COUNT(a.name) DESC
        LIMIT 4 ''');
    result = cur.fetchall()
    Totals = [item for t in result for item in t]
    print(Totals)

    labels = ContentRating
    explode = (0.1, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(Totals, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, rotatelabels= 0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Percentage of Apps in Each Content Rating")
    plt.show()

def scatterplot():
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT a.Price
        FROM Apps a
        Order by Price DESC''');
    result = cur.fetchall()
    ContentRating = [item for t in result for item in t]
    print(ContentRating)

    cur.execute('''SELECT a.Rating
        FROM Apps a
        Order by Price DESC ''');
    result = cur.fetchall()
    Totals = [item for t in result for item in t]
    print(Totals)

    plt.scatter(ContentRating,Totals, edgecolors='r')
    plt.xlabel('Price')
    plt.ylabel('Rating')
    plt.title('Correlation between Price and Rating')
    plt.xticks(fontsize=8, rotation=90)
    plt.show()

def line_chart2():
    s = [1,2,3,4,5]
    s2 = [1,2,3,4,5]
    plt.plot(s, s2)

    plt.xlabel('Item (s)')
    plt.ylabel('Value')
    plt.title('Python Line Chart: Plotting numbers')
    plt.grid(True)
    plt.show()


scatterplot()
reviews_bargraph()
Category_piechart()
contentrating_piechart()

cur.close();
cnx.commit();
cnx.close();