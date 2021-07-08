#!/usr/bin/python3

import re
from zipfile import ZipFile

#z = ZipFile("2021-07-07T164414_VeeamBackupLogs.zip", "r")
z = ZipFile("2021-07-07T161552_VeeamBackupLogs.zip", "r")
#p = re.compile(".*[^A-Z]IP.*")
#p = re.compile(".*[^A-Z]IP.*", re.IGNORECASE)
#p = re.compile(".*Error.*", re.IGNORECASE)

## Patterns
# String pattern
p = re.compile(".*(Error|Warning)  .*")

# File name pattern
fileP = re.compile(".*Job.*log")

## Flags
isPreviousLineError = 0
linesWithoutError = 1
isFileClear = 1

for filename in z.namelist():
    #if 'Job.TinyVM_backup.Backup.log' in filename:
    #print(filename) 

    # match for file name pattern
    mFileP = fileP.match(filename)
    if mFileP:
       isFileClear = 1
       print('File:', filename)
       bytes = z.read(filename)
       print('Size', round(len(bytes)/1024/1024,2), 'MB', '\n')
       for line in bytes.decode('utf-8').split('\n'):
           if not (isPreviousLineError or (linesWithoutError > 1)) :
               print('...')
           m = p.match(line)
           if m:
               print(m.group())
               isPreviousLineError = 1
               linesWithoutError = 0
               isFileClear = 0
           else:
               isPreviousLineError = 0
               linesWithoutError += 1 
       
       if isFileClear:
           print("No errors were found")
       print()
       print('-' * 30, '\n')
