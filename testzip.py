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



pattern_vbr_version = 'version: \[(.*)\], Assembly'



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


  # Counters
  depth = 2
  depth_counter = 0

  # Lists
  reversed_out_list = []
  out_list = []


  # Output lines
  reversed_out = ''

  m_file_p = file_p.match(filename)
  if m_file_p:
    is_file_clear = 1
    # add log file name to a file then apped the matched to a reversed list

    #reversed_out_list.append(str('File: ' + filename))
    #reversed_out_list = ['10', '8', '5', '2', '1']
    # print('File:', filename)
    bytes_archive = z.read(filename)

    # Add file name
    file_name = "File: " + filename
    out_list.append(file_name)
    
    # Add file size
    # print('Size', round(len(bytes_archive)/1024/1024,2), 'MB', '\n')
    file_size = 'Size: ' + str(round(len(bytes_archive)/1024/1024,2)) + ' MB' + '\n'
    out_list.append(file_size)
    #print(out_list[-1])



    string_list = bytes_archive.decode('utf-8').split('\n')

    # go through lines in straight order
    #for line in string_list:
    # go through lines in reverse order
    for line in reversed(string_list):
      if not (is_previous_line_error or (lines_without_error > 1)):  #and depth_counter < depth:
        #print('...')
        reversed_out_list.append('...')
        depth_counter += 1
        #print(f"depth is {depth}")
        #print(f"depth_counter is {depth_counter}")
        if depth_counter > depth:
            #print(f"DEPTH OF {depth_counter - 1} reached")
            break
        #print(reversed_out_list)

      m = p.match(line)
      #m2 = p2.match(line)
      m2 = re.search(pattern_vbr_version, line)
#      if m2:
#        print(m2.group(1))

      if m:
        #print(m.group())
        reversed_out_list.append(m.group())
        is_previous_line_error = 1
        lines_without_error = 0
        is_file_clear = 0
      else:
        is_previous_line_error = 0
        lines_without_error += 1 
     
    if is_file_clear:
      out_list.append("No errors were found")
      #print("No errors were found")
    delimiter = '\n' + ('-' * 30) + '\n'
    #print()
    #print(delimiter)
    #print('-' * 30, '\n')
#    return(reversed_out_list)

    #print(reversed_out_list)

    #reversed_out_list = ['10', '8', '5', '2', '1']

    while reversed_out_list:
      out_list.append(reversed_out_list.pop())
      #print(reversed_out_list.pop())

    out_list.append(delimiter)

    for i in out_list:
        print(i)


for filename in z.namelist():
  #if 'Job.TinyVM_backup.Backup.log' in filename:
  #print(filename) 

  # match for file name pattern
  match_file_pattern(filename)

