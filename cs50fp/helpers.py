import subprocess
import sqlite3

from datetime import datetime


# Working on the assumption that all texts are of equal value. Going forward weights may be considered
# Have separate C file to run hash table constantly with the main one analyzing texts one by one?
# ^ Potential to expand into multithreaded usage with multiple calls at the time?


def callC(args):
    '''
    Takes a list of strings as a argument, calls C script for analysis
    Returns a list of tuples with text valences (float) and number of words analyzed per each (int)
    '''
    
    command = ['./backend'] + args
    result = subprocess.run(command, capture_output = True, text = True)

    valences = []
    i = 0
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n'):
            data = line.split(';')
            rounded = round(float(data[1]), 8)
            valences.append((rounded, int(data[2])))
            if i != int(data[0]):
                return "Missing or escessive data in C script output"
            i += 1 
        return valences
    else:
        return result.stderr.strip()
    
    

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
        connector.rollback()
        return f"{e}"

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
                                texts.batch_id AS id,
                                batches.topic AS topic,
                                batches.size AS size,
                                batches.datetime AS datetime,
                                AVG(texts.valence) AS avg_valence,
                                AVG(texts.analyzed_words) AS avg_analyzed_words,
                                AVG(length(texts.content)) AS avg_symbols
                            FROM texts
                            JOIN batches
                            ON texts.batch_id = batches.id
                            GROUP BY batch_id 
                            ORDER BY batch_id DESC;
                        ''')
        
        theList = cursor.fetchall()

        connector.commit()

    except sqlite3.Error as e:
        connector.rollback()
        return f"{e}"

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
        connector.rollback()
        return f"{e}"

    finally:
        if connector:
            connector.close()

    return theList