import subprocess

# Replace dict with list? The former is a bit redundant
# How do I pass multiple large texts to C though?
# Have separate C file to run hash table constantly with the main one analyzing texts one by one

def callC(args):
    '''
    Takes a list of strings as a argument
    Returns a dict of text indexes (ints) and their valences (floats)
    '''
    
    command = "./clangout"
    for arg in args:
        command += " " + arg + " "
    
    result = subprocess.run([command], capture_output = True, text = True)

    valences = {}
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n'):
            data = line.split(',')
            valences[int(data[0])] = float(data[1])
        return valences
    else:
        return "Error: " + result.stderr.strip()
    
# def SQL adder
# def SQL fetcher