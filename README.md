# log-parser3000
A log parser for Veeam Backup and Replication log bundles written in Python3.


Usage

run with:
./log-parser3000 [OPTION] [FILE] 

[DESCRIPTION]

-d [depth] 
    sets depth flag

-j=N
    looks for last N jobs. Default value is 1 (last job details, such as version, job options, etc). When set to 0 it will print details for all jobs.

-e=N 
    looks for last N error stacks. Default value is 1 (last error stack)


!!! Need to use Job as a main working entity, not list of all strings in job.

Wrong:
Whole file (string) >> split to strings by '\n' (one line - one string) >> List of all strings in file >> List of all strings in job

Correct:
Whole file (string) >> split to strings by '==========' (one job - one string) >> put job-strings to list >> pick a N job-string >> List of all strings in job

Intermediate output:
list_job_strings = [job_string1, job_string2, ..., job_stringN]

#Pick job-string, split it to strings by '\n', put them to list of all strings for current job
job_string >> list_job_strings
list_job_strings = [version_string, job_options_string, [error_stack1_string, error_stack2_string]]

# We can later pick the certain number of last N jobs
list_job_strings[-N:]

# Example for picking last 2 elements 
N = 2
my_string = [12, 23, 34, 45]
my_string[-N:]
[34, 45]


Process

Final output



depth - the number of uninterrupted error stack, 0 - looks for all error lines, 1 - default value, looks for the latest error stack


match_list - list of matched strings

matches - strings matched by regex
  vbr_version
  start_time
  error_stack   # e.g. "string Error 1 \nstring Error 2 \nstring Error 3"

By setting the depth '-dj N' we can put last N jobs 
