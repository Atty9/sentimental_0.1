import subprocess
import sqlite3

from datetime import datetime

# Fix i iteration in output.html

# Display average valence of the set of texts given 
# Limit digits of the valences
# Add topic input
# Need to add to C output: size of each text, valence 0 if there was nothing to analyze
# Create details.html


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
            valences.append((float(data[1]), int(data[2])))
            if i != int(data[0]):
                return "Error: Missing output from C script"
            i += 1 
        return valences
    else:
        return "Error: " + result.stderr.strip()
    
    

def sqlInserter(texts, output):
    # texts is a list of strings
    # output is dict of indexes and valences (all type string)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    connector = sqlite3.connect('history.db')
    cursor = connector.cursor()

    # topic

    # Calculating average valence of the batch
    counter = 0
    total = 0.0
    for key, value in output.items():
        try:
            value = float(value)
        except ValueError:
            pass
        else:
            counter += 1
            total += value
    if counter == 0:
        avg_valence = 0
    else:
        avg_valence = total / counter



    cursor.execute('''INSERT INTO analyses (
                            topic, 
                            avg_valence, 
                            avg_text_size, 
                            batch_size,
                            datetime
                    ) VALUES (

                            
                    );

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

    