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
error_depth = 0
job_depth = 0

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
    # Error string pattern
    pattern = re.compile(".*(Error)  .*")

    # File name pattern
    file_p = re.compile(".*Job.*log")

    ## Flags
    is_previous_line_error = 0
    lines_without_error = 0


    # Counters
    error_depth_counter = 0
    job_depth_counter = 0

    # Lists
    #reversed_out_list = []
    out_list = []


    m_file_p = file_p.match(filename)
    if m_file_p:
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
      #list_job_strings = bytes_archive.decode('utf-8').split('\n')
      job_list = bytes_archive.decode('utf-8').split('Starting new log')
      #job_list = bytes_archive.decode('utf-8').split('===================================================================')

      error_stack_list = [] 
      out_job_list = []
  
      for job in job_list:
          job_strings_list = job.split('\n')
          #print(f"NEW JOB: \n {job}")

          # Error lines of one stack will be concatenated to this string
          error_stack = ''
          
          # go through lines in straight order
          for line in job_strings_list:
            #print(f"NEW JOB: \n {line}")
            #print(f"*{line}")
            
            #---------------
            match_job_start_time = re.search(pattern_job_start_time, line)
            if match_job_start_time:
              out_list.append('Start time: ' + match_job_start_time.group(1) + '\n')
              out_job_list.append('Start time: ' + match_job_start_time.group(1) + '\n')


            match_vbr_version = re.search(pattern_vbr_version, line)
            if match_vbr_version:
              out_list.append('\nVBR version: ' + match_vbr_version.group(1))
              out_job_list.append('\nVBR version: ' + match_vbr_version.group(1))
              job_depth_counter += 1
              if job_depth != 0 and job_depth_counter >= job_depth:
                break
            #---------------
            
             
            if not is_previous_line_error or not (lines_without_error > 1):
              #print('...')
              error_stack_list.append(error_stack)
              error_stack = ''
              #error_depth_counter += 1
              #print(f"depth is {depth}")
              #print(f"depth_counter is {depth_counter}")

              #if error_depth != 0 and error_depth_counter >= error_depth:
                  #print(f"DEPTH OF {depth_counter - 1} reached")
                  #break
      
            match_error = pattern.match(line)
      
            if match_error:
              # Grab the whole matching line and apped it to out list
              out_list.append(match_error.group())

              # Append new line and error line to error_stack
              #error_stack += '\n' + match_error.group()
              error_stack += match_error.group()
              print(f"New Error Stack: \n{error_stack}")
              is_previous_line_error = 1
              lines_without_error = 0
            else:
              is_previous_line_error = 0
              lines_without_error += 1 
           
          # Add a delimiter between files
          delimiter = '\n' + ('-' * 30) + '\n'
          out_list.append(delimiter)
  
      #for i in out_list:
          #print(i)
  
      #for i in error_stack_list:
          #print(i)
  
match_file_pattern(archive_name, error_depth, job_depth)
