# log-parser3000
A log parser for Veeam Backup and Replication log bundles written in Python3.


Usage

run with:
./log-parser3000 -f [archive_name] -d [depth]


depth - the number of uninterrupted error stack, 0 - looks for all error lines, 1 - default value, looks for the latest error stack
