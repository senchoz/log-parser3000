#!/usr/bin/python3

import re
from zipfile import ZipFile

z = ZipFile("2021-07-07T164414_VeeamBackupLogs.zip", "r")
#z = ZipFile("2021-07-07T161552_VeeamBackupLogs.zip", "r")
#pattern = 'us.r'
pattern = 'ipa'
#p = re.compile('ipa', re.IGNORECASE)
#p = re.compile(".*[^A-Z]IP.*")
#p = re.compile(".*[^A-Z]IP.*", re.IGNORECASE)
#p = re.compile(".*Error.*", re.IGNORECASE)
p = re.compile(".*Error  .*")

isPreviousLineError = 0
linesWithoutError = 0
#p = re.search('us.r')

#txt = "The rain in Spain\nThe rain in Brazil"
#x = re.search("^The.*Spain", txt)

for filename in z.namelist():
    if 'Job' in filename:
       print('File:', filename)
       bytes = z.read(filename)
       print('Size', round(len(bytes)/1024/1024,2), 'MB', '\n')
       for line in bytes.decode('utf-8').split('\n'):

           # Regex applied to each line
           #match = re.search(pattern, line)
           #m = re.match(p, line)
           #print(p.match(line))
           #print(type(line))
           if not isPreviousLineError and (linesWithoutError == 0) :
               print('...')
           m = p.match(line)
           #m.group()
           if m:
               print(m.group())
               isPreviousLineError = 1
           #if match:
               # Make sure to add \n to display correctly
               #new_line = match.group() + '\n'
               #print(new_line)
               #print(line)
           else:
               isPreviousLineError = 0
               linesWithoutError += 1 
       
       count = 0
       print('\n')
       print('---','\n')
'''       for cult in Lines:
           count += 1
           print("Line{}: {}".format(count, line.strip()))'''

#print(x.string)
