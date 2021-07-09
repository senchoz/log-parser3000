#!/usr/bin/python3

import re
from zipfile import ZipFile
import os
from read_reverse_order import read_reverse_order


#logFile = open("job.log", "r")
log_file = open("job.log", "r")
#log_line = reverse_readline(log_file)
#log_line = read_reverse_order(log_file)
#print(logLine)
#print(read_reverse_order("job.log"))

# read file in reverse order
#for line in read_reverse_order("job.log"):
#  print(line)

#z = ZipFile("2021-07-07T164414_VeeamBackupLogs.zip", "r")
z = ZipFile("2021-07-07T161552_VeeamBackupLogs.zip", "r")
#p = re.compile(".*[^A-Z]IP.*")
#p = re.compile(".*[^A-Z]IP.*", re.IGNORECASE)
#p = re.compile(".*Error.*", re.IGNORECASE)



def match_file_pattern(filename):
  ## Patterns
  # String pattern
  p = re.compile(".*(Error)  .*")
  p2 = re.compile(".*Backup.Manager.*File version: \[[0-9].*\]")
  #p = re.compile(".*(Error|Warning)  .*")

  # File name pattern
  file_p = re.compile(".*Job.*log")

  ## Flags
  is_previous_line_error = 0
  lines_without_error = 1
  is_file_clear = 1

  # Lists
  reversed_out_list = []

  m_file_p = file_p.match(filename)
  if m_file_p:
    is_file_clear = 1
    reversed_out_list.append(str('File: ' + filename))
    print('File:', filename)
    bytes_archive = z.read(filename)
    #print(bytes_archive.decode('utf-8'))
    # Print file size
    print('Size', round(len(bytes_archive)/1024/1024,2), 'MB', '\n')
    string_list = bytes_archive.decode('utf-8').split('\n')
    for line in string_list:
    #for line in reversed(string_list):
    #for line in bytes.decode('utf-8').split('\n'):
    #print(type(bytes.decode('utf-8')))
    #for line in read_reverse_order(bytes.decode('utf-8')):
      if not (is_previous_line_error or (lines_without_error > 1)) :
        print('...')
        reversed_out_list.append('...')
        print(reversed_out_list)

      m = p.match(line)
      #m2 = p2.match(line)
      m2 = re.search('version: \[(.*)\], Assembly', line)
      if m2:
        #print(m2.match("File version: \[[0-9].*\]"))
        print(m2.group(1))

      if m:
        print(m.group())
        is_previous_line_error = 1
        lines_without_error = 0
        is_file_clear = 0
      else:
        is_previous_line_error = 0
        lines_without_error += 1 
     
    if is_file_clear:
      print("No errors were found")
    print()
    print('-' * 30, '\n')
    return(reversed_out_list)


for filename in z.namelist():
  #if 'Job.TinyVM_backup.Backup.log' in filename:
  #print(filename) 

  # match for file name pattern
  match_file_pattern(filename)


