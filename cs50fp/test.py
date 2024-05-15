import subprocess

args = ['giga', 'great terrible abandon the shop']

command = './clangout'
for arg in args:
    command += ' ' + arg + ' '
    
result = subprocess.run([command], capture_output = True, text = True)

valences = {}
if result.returncode == 0:
    for line in result.stdout.strip().split('\n'):
        data = line.split(',')
        valences[int(data[0])] = float(data[1])
    print(valences)
else:
    print("Error: " + result.stderr.strip())
    