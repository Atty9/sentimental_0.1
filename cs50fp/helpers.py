import subprocess
import sqlite3

from datetime import datetime

# Display average valence of the set of texts given 
# Limit digits of the valences
# Need to add a topic input for each batch
# Create details.html
# Get datetime.now

# Have separate C file to run hash table constantly with the main one analyzing texts one by one?
# ^ Potential to expand into multithreaded usage with multiple calls at the time

def callC(args):
    '''
    Takes a list of strings as a argument
    Returns a dict of text indexes (ints) and their valences (floats)
    
    Manually tracking indexes in C to track any skips, therefore dict here and not list
    '''
    
    command = ['./backend'] + args

    result = subprocess.run(command, capture_output = True, text = True)

    valences = {}
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n'):
            data = line.split(',')
            valences[data[0]] = data[1]
        return valences
    else:
        return "Error: " + result.stderr.strip()
    
def sqlInserter(texts, output):
    # texts is a list of strings
    # output is dict of indexes and valences (all type string)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    connector = sqlite3.connect('history.db')
    cursor = connector.cursor()

    cursor.execute('''INSERT INTO analyses (
                          topic,
                        

                      ) 
                      VALUES ();

    topic TEXT NOT NULL,
    avg_valence REAL NOT NULL, 
    avg_text_size REAL NOT NULL,
    batch_size INTEGER,
    datetime TEXT


    ''')



    # get current date and time
    # add data to analyses table
    # table 1: ITER INT id (unique), INT number of texts, TXT topic, DT date time, FLT? avg valence
    # get batch id from table 1 to use in table 2
    # table 2: ITER INT local id, INT batch number (ref id of table 1), FLT? valence, TXT text itself
    
    return

'''





'''

def sqlSelector():
    # fetch all data off table 1
    
    return # Dict of data

def sqlDetailedSelector(id):
    # fetch data off both tables for a selected single batch id

    return # Dict of data
