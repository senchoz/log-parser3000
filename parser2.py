#!/usr/bin/python3

import re

f = open("job.log", "r")
file_data = f.read()
list_jobs = file_data.split('Starting new log')

job = list_jobs[-1]

job_depth = 2


def parse_job(job):

    version = ''
    options = 'opt1'
    stack_list = []
    date = "tuesday"

    job_dict = { "Date" : date, "Version" : version, "Options" : options, "Stacks" : stack_list}


    stack_depth = 2
    error_stack = ''

    pattern_vbr_version = 'version: \[(.*)\], Assembly'
    pattern_job_start_time = 'start time: \[(.*)\],'
    pattern = re.compile(".*(Error)  .*")

    list_job_strings = job.splitlines()
    for job_string in list_job_strings:

        ## Version matching >>>

        match_vbr_version = re.search(pattern_vbr_version, job_string)
        if match_vbr_version:
            job_dict["Version"] = match_vbr_version.group(1)

        ## Version matching <<<


        ## Error matching >>>

        match_error = pattern.match(job_string)
        if match_error:
            error_stack += match_error.group() + '\n'
        elif error_stack:
            print("Appending current error stack")
            stack_list.append(error_stack)
            error_stack = ''

        ## Error matching <<<

    ## Error matching >>>

    if error_stack:
        print("Appending current error stack")
        stack_list.append(error_stack)

    ## Error matching <<<


    export_file= "output2.log"

    ## Writing output >>>

    with open(export_file, "a") as file:
        for element in job_dict.keys():
            if isinstance(job_dict[element], list):
                print(f"{element} (Last {stack_depth}):")
                file.write(f"{element} (Last {stack_depth}):\n")
                for error_stack in job_dict[element][-stack_depth:]:
                    print(error_stack)
                    file.write(error_stack + '\n')
            else:
                print(f"{element}:\n{job_dict[element]}\n")
                file.write(f"{element}:\n{job_dict[element]}\n")
            file.write('\n')

        file.write('=' * 30 + '\n')
        file.close

    ## Writing output <<<

#parse_job(job)

for job in list_jobs[-job_depth:]:
    parse_job(job)
