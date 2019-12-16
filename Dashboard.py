# Author: Joey Mannarino and Giovanni Grecco
# Milestone 3 Assignment
# 12/6/2019
# *finished Draft*


import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import numpy as np

# Connecting to the AWS database using the host and correct credentials
def make_connection():
    return pymysql.connect(host='database.c24by8ob2wiy.us-east-1.rds.amazonaws.com', user='admin', passwd='password',
                           port=3306, autocommit=True)


# making a open connection
cnx = make_connection()

# creating a cursor to execute statements
cur = cnx.cursor()


def reviews_bargraph(plt):
    # execute SQL statement
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT a.name
        FROM Apps a
        GROUP BY a.name
        ORDER BY Reviews DESC
        LIMIT 5 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn the results into a list
    names = [item for t in result for item in t]

    # execute SQL statement
    cur.execute('''SELECT a.Reviews
        FROM Apps a
        GROUP BY a.name
        ORDER BY Reviews DESC
        LIMIT 5 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn the results into a list
    reviews = [item for t in result for item in t]


    # Create bars and choose color
    plt.subplot(2, 3, 1)
    plt.barh(names, reviews, color=('green'))

    # Add title and axis names
    plt.title('Most Reviewed Apps')
    plt.ylabel('Apps')
    plt.xlabel('Reviews (10 Milion)')
    #set background color
    ax = plt.gca()
    ax.set_facecolor('#DBDCDB')




def Category_piechart(plt):
    # execute SQL statement
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT c.Category
        FROM Apps a, Category c
        WHERE a.CategoryID = c.CategoryID
        GROUP BY c.Category
        ORDER BY COUNT(a.name) DESC
        LIMIT 5 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    Categories = [item for t in result for item in t]

    #Execute SQL Statement
    cur.execute('''SELECT COUNT(a.name) as TotalApps
        FROM Apps a, Category c
        WHERE a.CategoryID = c.CategoryID
        GROUP BY c.Category
        ORDER BY COUNT(a.name) DESC
        LIMIT 5 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    Totals = [item for t in result for item in t]

    explode = (0.1, 0, 0, 0, 0)  # only "explode" the 1st slice (i.e. 'Family')
    plt.subplot(2,3,2)
    # create pie chart with set parameters
    plt.pie(Totals, explode=explode, labels=Categories, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Add title
    plt.title("Apps in Each Category")
    # set background color
    ax = plt.gca()
    ax.set_facecolor('#DBDCDB')

def contentrating_piechart(plt):
    # Execute SQL statement
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT a.ContentRating
        FROM Apps a
        GROUP BY a.ContentRating
        ORDER BY COUNT(a.name) DESC
        LIMIT 4''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    ContentRating = [item for t in result for item in t]

    # Execute SQL statement
    cur.execute('''SELECT COUNT(a.name) as TotalApps
        FROM Apps a
        GROUP BY a.ContentRating
        ORDER BY COUNT(a.name) DESC
        LIMIT 4 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    Totals = [item for t in result for item in t]

    colors = ['green', '#66b3ff', '#99ff99', '#ff9999'] # Specify color scheme of pie chart
    plt.subplot(2,3,3)
    # Create pie chart with set parameters
    plt.pie(Totals, colors = colors, autopct='%1.1f%%', startangle=90)
    # Create a center circle in the pie chart
    centre_circle = plt.Circle((0, 0), 0.75, fc='#DBDCDB')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Create and add a legend to the subplot
    plt.legend(ContentRating, bbox_to_anchor=(0.85, 1.025), loc="upper left")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Add title
    plt.title("Apps in Each Content Rating")
    # Set background color
    ax = plt.gca()
    ax.set_facecolor('#DBDCDB')

def scatterplot(plt):
    # Execute SQL statement
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT a.Reviews
        FROM Apps a
        Order by Price DESC''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    Reviews = [item for t in result for item in t]

    # Execute SQL statement
    cur.execute('''SELECT a.Rating
        FROM Apps a
        Order by Price DESC ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    Ratings = [item for t in result for item in t]

    plt.subplot(2,3,4)
    # Create scatter plot
    plt.scatter(Reviews, Ratings, color='green')
    # Add axis titles and labels
    plt.xlabel('Price')
    plt.ylabel('Rating')
    plt.title('Correlation between Price and Rating')
    # Set background color
    ax = plt.gca()
    ax.set_facecolor('#DBDCDB')

def installs_graph(plt):
    # Execute SQL statement
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT g.genre
        FROM Apps a, Genres g, GenreApp ga
        WHERE a.appId = ga.appId
        AND g.genreId = ga.genreId
        GROUP BY g.genre
        ORDER BY a.Installs DESC
        LIMIT 5 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    genres = [item for t in result for item in t]

    # Execute SQL statement
    cur.execute('''SELECT AVG(a.installs)
        FROM Apps a, Genres g, GenreApp ga
        WHERE a.appId = ga.appId
        AND g.genreId = ga.genreId
        GROUP BY g.genre
        ORDER BY a.Installs DESC
        LIMIT 5 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    installs = [item for t in result for item in t]

    y_pos = np.arange(len(genres))
    plt.subplot(2, 3, 5)
    # Create plot and choose color
    plt.plot(genres, installs, color=('green'))

    # Add title and axis names
    plt.title('Average installs per genre')
    plt.xlabel('Genres')
    plt.ylabel('Installs (10 Million)')

    # Limits for the Y axis
    plt.ylim(0, 35000000)

    # Create names
    plt.xticks(y_pos, genres)
    plt.xticks(rotation=90)
    # Set background color
    ax = plt.gca()
    ax.set_facecolor('#DBDCDB')

def ratingsGenre_graph(plt):
    # Execute SQL statement
    cur.execute('USE GoogleAppDB');
    cur.execute('''SELECT g.genre
        FROM Apps a, Genres g, GenreApp ga
        WHERE a.appId = ga.appId
        AND g.genreId = ga.genreId
        GROUP BY g.genre
        ORDER BY a.rating DESC
        LIMIT 10 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    genres = [item for t in result for item in t]

    # Execute SQL statement
    cur.execute('''SELECT AVG(a.rating)
        FROM Apps a, Genres g, GenreApp ga
        WHERE a.appId = ga.appId
        AND g.genreId = ga.genreId
        GROUP BY g.genre
        ORDER BY a.rating DESC
        LIMIT 10 ''');
    # Fetch results of SQL statement
    result = cur.fetchall()
    # Turn results into a list
    rating = [item for t in result for item in t]

    y_pos = np.arange(len(genres))
    plt.subplot(2, 3, 6)
    # create stem plot with set parameters
    (markerline, stemlines, baseline) = plt.stem(genres, rating,use_line_collection = True)
    plt.setp(baseline, visible=False)
    # Set color of stem-lines
    plt.setp(stemlines, visible=True, color='green')

    # Add title and axis names
    plt.title('Average Rating per genre')
    plt.xlabel('Genre')
    plt.ylabel('Rating')

    # Limits for the Y axis
    plt.ylim(0, 5.0)

    # Create names
    plt.xticks(y_pos, genres)
    plt.xticks(rotation=90)
    # Set background color
    ax = plt.gca()
    ax.set_facecolor('#DBDCDB')

fig = plt.figure(figsize=(15,8)) # Set size of each graph in the global plot
fig.set_facecolor('#DBDCDB') # Set background color of global plot

# Call the modules for each graph
ratingsGenre_graph(plt)
installs_graph(plt)
scatterplot(plt)
reviews_bargraph(plt)
Category_piechart(plt)
contentrating_piechart(plt)
plt.tight_layout()

# Show the graphs in a window
plt.show()
# Closing the cursor
cur.close();
cnx.commit();
# Closing the connection
cnx.close();