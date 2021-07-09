#!/usr/bin/python3

import re
from zipfile import ZipFile
import os
from read_reverse_order import read_reverse_order


#log_file = open("job.log", "r")

# read file in reverse order
# not applicable as it's an archive, but still may be useful in future
# it uses 1 string size buffer, therefore there's no need to open the whole file
#for line in read_reverse_order("job.log"):
#  print(line)


# Initial variables

# Set depth value
#error_depth = 3
error_depth = 1
job_depth = 1

archive_name = "2021-07-07T161552_VeeamBackupLogs.zip"

pattern_vbr_version = 'version: \[(.*)\], Assembly'
pattern_job_start_time = 'start time: \[(.*)\],'

# converts the time the job starts (e.g. 21/11/06 6:30:20 PM) from string to datetime format
#dt_job_start_time = datetime.strptime("21/11/06 6:30:20 PM", "%d/%m/%y %I:%M:%S %p")



def match_file_pattern(archive_name, error_depth, job_depth):
  z = ZipFile(archive_name, "r")
  for filename in z.namelist():
    # match for file name pattern
    #match_file_pattern(filename)

    ## Patterns
    # String pattern
    p = re.compile(".*(Error)  .*")
    p2 = re.compile(".*Backup.Manager.*File version: \[[0-9].*\]")
    #p = re.compile(".*(Error|Warning)  .*")

    # File name pattern
    file_p = re.compile(".*Job.*log")

    ## Flags
    is_previous_line_error = 0
    lines_without_error = 0
    is_file_clear = 1


    # Counters
    error_depth_counter = 0
    job_depth_counter = 0

    # Lists
    reversed_out_list = []
    out_list = []


    m_file_p = file_p.match(filename)
    if m_file_p:
      is_file_clear = 1
      # add log file name to a file then append the matched to a reversed list

      # print('File:', filename)
      bytes_archive = z.read(filename)
  
      # Add file name
      file_name = "File: " + filename
      out_list.append(file_name)
      
      # Add file size
      file_size = 'Size: ' + str(round(len(bytes_archive)/1024/1024,2)) + ' MB' + '\n'
      out_list.append(file_size)
  
  
      # Decode bytes for current log file in archive 
      # Split the decoded bytes to strings
      # Add them to a new list
      string_list = bytes_archive.decode('utf-8').split('\n')
  
      # go through lines in straight order
      #for line in string_list:

      # go through lines in reverse order
      for line in reversed(string_list):

        #match_job_start_time = re.search(pattern_job_start_time, line)
        #if match_job_start_time:
        #  out_list.append('Start time: ' + match_job_start_time.group(1))
         
        #match_vbr_version = re.search(pattern_vbr_version, line)
        #if match_vbr_version:
        #  out_list.append('VBR version: ' + match_vbr_version.group(1) + '\n')
        #  pass
        
        #---------------
        match_vbr_version = re.search(pattern_vbr_version, line)
        if match_vbr_version:
          reversed_out_list.append('\nVBR version: ' + match_vbr_version.group(1))
          #if job_depth_counter > job_depth:
          job_depth_counter += 1
          if job_depth != 0 and job_depth_counter >= job_depth:
            break

        match_job_start_time = re.search(pattern_job_start_time, line)
        if match_job_start_time:
          reversed_out_list.append('Start time: ' + match_job_start_time.group(1) + '\n')
        #---------------
        
         
        if not (is_previous_line_error or (lines_without_error > 1)) and not is_file_clear: 
          #print('...')
          reversed_out_list.append('...')
          error_depth_counter += 1
          #print(f"depth is {depth}")
          #print(f"depth_counter is {depth_counter}")
          #if not (error_depth != 0 or error_depth_counter > error_depth):
          if error_depth != 0 and error_depth_counter >= error_depth:
              #print(f"DEPTH OF {depth_counter - 1} reached")
              break
  
        m = p.match(line)
  
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
  
  
      while reversed_out_list:
        out_list.append(reversed_out_list.pop())
  
      # Add a delimiter between files
      delimiter = '\n' + ('-' * 30) + '\n'
      out_list.append(delimiter)
  
      for i in out_list:
          print(i)
  
  
match_file_pattern(archive_name, error_depth, job_depth)
