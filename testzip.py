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

  #####################################################################
  # start going over matching files in archive
  #####################################################################

  for filename in z.namelist():
    # match for file name pattern
    #match_file_pattern(filename)

    ## Patterns
    # Error string pattern
    pattern = re.compile(".*(Error)  .*")

    # File name pattern
    file_pattern = re.compile(".*Job.*log")

    ## Flags
    is_previous_line_error = 0
    lines_without_error = 0
    is_file_clear = 1


    # Counters
    error_depth_counter = 0
    job_depth_counter = 0

    # Lists
    #reversed_out_list = []
    out_list = []

    error_stack_list = [] 
    out_job_list = []

    match_file_pattern = file_pattern.match(filename)




    if match_file_pattern:
      is_file_clear = 1
      # add log file name to a file then append the matched to a reversed list

      print('File:', filename)
      bytes_archive = z.read(filename)
  
      # Add file name
      file_name = "File: " + filename + '\n'
      out_list.append(file_name)
      out_job_list.append(file_name)
      
      # Add file size
      file_size = 'Size: ' + str(round(len(bytes_archive)/1024/1024,2)) + ' MB' + '\n'
      out_list.append(file_size)
      out_job_list.append(file_size)

      #file_elements = ['', [], 'vasyan']
      file_elements = ['', []]

      #file_list[0] += file_name + file_size
      file_elements[0] += file_name + file_size
      #file_details = file_elements[0] += file_name + file_size
      #file_details += file_name + file_size
      jobs = file_elements[1]

  
  
      # Decode bytes for current log file in archive 
      # Split the decoded bytes to strings
      # Add them to a new list
      #list_job_strings = bytes_archive.decode('utf-8').split('\n')
      job_list = bytes_archive.decode('utf-8').split('Starting new log')
      #job_list = bytes_archive.decode('utf-8').split('===================================================================')

      
      #####################################################################
      # start going over jobs in job list
      #####################################################################

      for job in job_list:
          job_strings_list = job.split('\n')
          #print(f"NEW JOB: \n {job}")

          # Error lines of one stack will be concatenated to this string
          error_stack = ''
           
          #####################################################################
          # start going over lines in job
          #####################################################################

          for line in job_strings_list:
            #print(f"NEW JOB: \n {line}")
            #print(f"*{line}")
            
            match_job_start_time = re.search(pattern_job_start_time, line)
            if match_job_start_time:
              out_list.append('Start time: ' + match_job_start_time.group(1) + '\n')
              out_job_list.append('Start time: ' + match_job_start_time.group(1) + '\n')
              jobs.append('Start time: ' + match_job_start_time.group(1) + '\n')


            match_vbr_version = re.search(pattern_vbr_version, line)
            if match_vbr_version:
              out_list.append('\nVBR version: ' + match_vbr_version.group(1))
              out_job_list.append('\nVBR version: ' + match_vbr_version.group(1))
              jobs.append('\nVBR version: ' + match_vbr_version.group(1))
              job_depth_counter += 1

              # If defined limit of jobs is reached in current file -> break out of the loop and jump to the next file
              if job_depth != 0 and job_depth_counter >= job_depth:
                break
            
            # A bit cumbersome statement. If current error stack is interrupted by non-error string, 
            # we add existing error stack to the list and nullify the current error stack
            # By default, the each file is treated as 'clear' (doesn't contain errors)
            if not is_previous_line_error and not (lines_without_error > 1) and not is_file_clear:
              error_stack_list.append(error_stack)
              error_stack = ''
      
            # Try to match the pattern over the line
            match_error = pattern.match(line)
      
            # Check if match occurred
            if match_error:
              # If the error is found the file is not 'clear' anymore
              is_file_clear = 0 

              # Grab the whole matching line and append it to jobs list
              out_list.append(match_error.group())
              out_job_list.append(match_error.group())
              jobs.append(match_error.group())


              # Append new line and error line to error_stack
              error_stack += '\n' + match_error.group()

              #error_stack += match_error.group()
              #print(f"New Error Stack: \n{error_stack}")
              is_previous_line_error = 1
              lines_without_error = 0
            else:
              is_previous_line_error = 0
              lines_without_error += 1 
           
          #####################################################################
          # stop going over lines in job
          #####################################################################

          #print(out_job_list)
          # Add a delimiter between files
          delimiter = '\n' + ('-' * 30) + '\n'
          out_list.append(delimiter)
          out_job_list.append(delimiter)
          #jobs.append(delimiter)
  
      #for i in out_job_list:
      #    print(i)
      #print(error_stack_list)
  
      error_depth = 3
      job_depth = 1

      # Working good, but only shows last N error stacks
      #for i in error_stack_list[-error_depth:]:
      #    print(i)

      #print(f"file_elements: {file_elements})")


      #####################################################################
      # stop going over jobs in job list
      #####################################################################

      # go over file details (such as, filename, file size, list of jobs)
      for file_element in file_elements:
          # if the element is list... 
          if isinstance(file_element, list):
              # ...start going over the jobs inside the list
              for job in file_element:
                  # for 
                  for job_element in job:
                      if isinstance(job_element, list):
                          for error_stack in job_element:
                              print(error_stack)
                      print(job_element)
          else:
              #print(file_element)
              print(f"file_element: {file_element})")
          #print(f"file_elements: {file_elements})")
      # Should return last N jobs and last M errors stacks
      #for job in out_job_list[-job_depth:]:
      #    print(job)
      #    for i in error_stack_list[-error_depth:]:
      #        print(i)

  #####################################################################
  # stop going over matching files in archive
  #####################################################################
  
match_file_pattern(archive_name, error_depth, job_depth)
