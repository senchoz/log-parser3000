#!/usr/bin/python3

import os
from zipfile import ZipFile
import re
import time
from time import strftime

def main():
    #log_file_path = r"C:\ios logs\sfbios.log"
    archive_file_path = "2021-07-07T161552_VeeamBackupLogs.zip"
    #export_file_path = r"output.log"
    export_file= "output.log"

    #pattern_job_start_time = 'start time: \[(.*)\],'

    time_now = str(strftime("%Y-%m-%d %H-%M-%S", time.localtime()))

    #file = "\\" + "Parser Output " + time_now + ".txt"
    export_file = export_file + "_" + time_now + ".txt"
    z = ZipFile(archive_file_path, "r")
    for filename in z.namelist():
        pattern_file = re.compile(".*Job.*log")

        match_file = pattern_file.match(filename)

        if match_file:
            # Decode bytes for current log file in archive
            # Split the decoded bytes to strings
            # Add them to a new list
            bytes_archive = z.read(filename)
            string_list = bytes_archive.decode('utf-8').split('\n')

            #regex = '(<property name="(.*?)">(.*?)<\/property>)'
            p_error = re.compile(".*(Error)  .*")

            #parseData(log_file_path, export_file, regex, read_line=True, reparse=True)
            parseData(string_list, export_file, p_error)


#def parseData(archive_file_path, export_file, regex, read_line=True, reparse=False):
def parseData(string_list, export_file, p_error):
    #string_list = bytes_archive.decode('utf-8').split('\n')
    #print(string_list)
    pattern_job_start_time = 'start time: \[(.*)\],'
    out_list = [[] for i in range(3)]
    #out_list = []
    for line in string_list:
        #print(line)
        match_job_start_time = re.search(pattern_job_start_time, line)
        if match_job_start_time:
            out_list[0].append('Start time: ' + match_job_start_time.group(1) + '\n')

        m_error = p_error.match(line)
        if m_error:
            out_list[2].append(m_error.group())
            #print(out_list)
            #print(match_job_start_time)
#    with open(log_file_path, "r") as file:
#        match_list = []
#        if read_line == True:
#            for line in file:
#                for match in re.finditer(regex, line, re.S):
#                    match_text = match.group()
#                    match_list.append(match_text)
#        else:
#            data = file.read()
#            for match in re.finditer(regex, data, re.S):
#                match_text = match.group();
#                match_list.append(match_text)
#    file.close()

#    if reparse == True:
#        match_list = reparseData(match_list, '(property name="(.{1,50})">(Enabled)<\/property>)')

    #with open(export_file, "w+") as file:
    with open(export_file, "a") as file:
        file.write("EXPORTED DATA:\n")
        #match_list_clean = list(set(match_list))
       ##match_list_clean = list(set(out_list))
        #for item in xrange(0, len(match_list_clean)):
        #for item in match_list_clean:

        # working fine with 1D list
        #for item in out_list:
        #    print(item)
        #    file.write(item + "\n")

        # working fine with 2D list
        for item in out_list:
        #    print(*item, sep='\n')
            #file.writelines('\t'.join(str(j + '\n') for j in i) + '\n' for i in out_list)
            file.writelines(''.join(str(j + '\n') for j in i) + '\n' for i in out_list)

    file.close()
    #return match_list_clean
    #return out_list

#def reparseData(parsed_data, regex):
#    data_string = ''.join(parsed_data)
#    match_list = [];
#    for match in re.finditer(regex, data_string, re.S):
#        match_text = match.group();
#        match_list.append(match_text)
#    return match_list

if __name__ == '__main__':
    main()

