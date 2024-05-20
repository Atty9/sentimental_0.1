import subprocess
import sqlite3

from datetime import datetime

# Fix i iteration in output.html

# DO I check sql db connection for failure? if == NULL
# Display average valence of the set of texts given
# Add topic input
# Need to add to C output: size of each text, valence 0 if there was nothing to analyze
# Create details.html
# WOrking on the assumption that all texts are of equal value. Going forward weights may be considered


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
            rounded = round(float(data[1]), 4)
            valences.append((rounded, int(data[2])))
            if i != int(data[0]):
                return "Error: Missing output from C script"
            i += 1 
        return valences
    else:
        return "Error: " + result.stderr.strip()
    
    

def sqlInserter(texts, output, topic):
    '''
    Takes list of texts before analysis, output of C analysis (list of tuples) and user provided topic
    Inserts data about analyzed batch into SQL history.db
    '''

    # connecting to the database
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

    return

def sqlSelector():
    '''
    Fethes data from sql database, returns general information for all analyzed batches
    '''

    # connecting to the database
    connector = sqlite3.connect('history.db')
    cursor = connector.cursor()

    cursor.execute('''SELECT  ''')
    '''
    SELECT
        id,
        topic,
        size, 
        datetime
    FROM batches
    JOIN texts 
    ON batches.id = texts.batch_id
    ;
    '''

    return # Dict of data

def sqlDetailedSelector(id):
    # fetch data off both tables for a selected single batch id

    return # Dict of data

'''
CREATE TABLE batches(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    topic TEXT NOT NULL,
    size INTEGER NOT NULL,
    datetime TEXT NOT NULL
);

SELECT FROM texts
    batch_id,
    AVG(valence) AS avg_valence,
    
    
GROUP BY batch_id,
DESC;

CREATE TABLE texts(
    local_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    batch_id INTEGER NOT NULL,
    valence REAL NOT NULL,
    analyzed_words INTEGER NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (batch_id)
    REFERENCES batches(id)
);
'''