import os

filenn = 'prep'
filename = '{}.txt'.format(filenn)
nfilename = '{}2.txt'.format(filenn)
wlist = []
with open(filename, 'r') as f:
    for line in f.readlines():
        line = line.strip()
        word = line.split('、')
        wlist += word
        print(word)

with open(nfilename, 'w') as f:
    for item in wlist:
        f.write(item+'\n')

