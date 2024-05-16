import subprocess

# Display average valence of the set of texts given 
# Limit digits of the valences
# Need to add a topic input to easil

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
    # get current date and time
    # 
    # table 1: ITER INT id (unique), INT number of texts, TXT topic, DT date time, FLT? avg valence
    # table 2: ITER INT local id, INT batch number (ref id of table 1), FLT? valence, TXT text itself
    
    return

def sqlSelector():
    # fetch all data off table 1
    
    return # Dict of data

def sqlDetailedSelector(id):
    # fetch data off both tables for a selected single batch id

    return # Dict of data
