import sqlite3
from datetime import datetime


def sqlInserter(texts, output, topic):
    '''
    Takes list of texts before analysis, output of C analysis (list of tuples) and user provided topic
    Inserts data about analyzed batch into SQL history.db
    '''
    
    try:
        # Connecting to the database
        connector = sqlite3.connect('history.db')
        cursor = connector.cursor()

        # Getting batch size
        size = len(texts)

        # Getting current date and time as a string
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Inserting into the first table of history.db
        cursor.execute('''INSERT INTO batches (topic, size, datetime) 
                        VALUES (?, ?, ?);''', (topic, size, now))

        # Getting batch id generated in the first table
        batch_id = cursor.lastrowid

        # Inserting data into the second table
        i = 0
        listlen = len(texts)
        while i < listlen:
            cursor.execute('''INSERT INTO texts (batch_id, valence, analyzed_words, content) 
                            VALUES (?, ?, ?, ?);''', (batch_id, output[i][0], output[i][1], texts[i]))
            i += 1

        connector.commit()

    except sqlite3.Error as e:
        print(f"Error: {e}")
        connector.rollback()

    finally:
        if connector:
            connector.close()

    return


def sqlSelector():
    '''
    Returns general information for all analyzed batches from sql db as a list of tuples
    '''

    try:
        # Connecting to the database
        connector = sqlite3.connect('history.db')
        cursor = connector.cursor()

        # Fetching relevant data as a list of tuples
        cursor.execute('''  
                            SELECT
                                texts.batch_id,
                                batches.topic AS topic,
                                batches.size AS size,
                                batches.datetime AS datetime,
                                AVG(texts.valence) AS avg_valence,
                                AVG(texts.analyzed_words) AS avg_analyzed_words,
                                AVG(length(texts.content)) AS symbols
                            FROM texts
                            JOIN batches
                            ON texts.batch_id = batches.id
                            GROUP BY batch_id 
                            ORDER BY batch_id DESC;
                        ''')
        
        theList = cursor.fetchall()

        connector.commit()

    except sqlite3.Error as e:
        print(f"Error: {e}")
        connector.rollback()

    finally:
        if connector:
            connector.close()

    return theList


def sqlDetailedSelector(id):
    '''
    Takes in batch id
    Returns detailed data on the batch with that id (as a list of tuples)
    '''

    try:
        # Connecting to the database
        connector = sqlite3.connect('history.db')
        cursor = connector.cursor()

        # Fetching details of the batch from texts table
        cursor.execute('''
                        SELECT 
                            valence,
                            analyzed_words,
                            content
                        FROM texts
                        WHERE batch_id = ?
                        ''', (id,))
        
        theList = cursor.fetchall()

        connector.commit()

    except sqlite3.Error as e:
        print(f"Error: {e}")
        connector.rollback()

    finally:
        if connector:
            connector.close()

    return theList


texts = ["test giga duper test tasty test, mmm", "giag giga gia gia giga", "test 3 mate"]
output = [(4.5,4),(0.0,0),(3,1)]
topic = "giga"

print("Inserter call next")

sqlInserter(texts, output, topic)

print("sqlSelector output below")

print(sqlSelector())

print("sqlDetailedSelector output below")

print(sqlDetailedSelector(1))