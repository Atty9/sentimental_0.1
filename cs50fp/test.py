import subprocess


def callC(args):

    command = ['./backend'] + args

    result = subprocess.run(command, capture_output = True, text = True)

    valences = []
    i = 0
    if result.returncode == 0:
        print(result.stdout)
        for line in result.stdout.strip().split('\n'):
            print(line)
            data = line.split(';')
            print(data)
            valences.append((float(data[1]), int(data[2])))
            if i != int(data[0]):
                return "Error: Missing output from C script"
            i += 1 
        return valences
    else:
        return "Error: " + result.stderr.strip()
    

theList = ["great love it amazing aspiring god", "giga giga giga", "terrible do not hate sucks"]
print(callC(theList))