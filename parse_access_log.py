#!/usr/bin/env python

import os
import re
from collections import Counter

access_log_file = "access.log"
prev_file = "access.log_prev"

# regex for http calls in access.log
lineformat = re.compile(
    r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((?P<method>\"(GET|HEAD|POST|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH))(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""",
    re.IGNORECASE)




def get_calls_uniq_counter(access_log_filename):
    '''
    This method scan all file lines , using regex to extract HTTP Calls.
    Build a list of all HTTP-calls that match the regex .
    Calculate the uniq counts for each call by using collections.Counter method .

    :param file: access.log_prev file to calculate the uniq calls
    :return: tuple [total_calls , Counter(calls)]
    '''

    calls = []
    with open(access_log_filename, 'r') as file:
        for l in file.readlines():
            data = re.search(lineformat, l)
            if data:
                datadict = data.groupdict()
                url = datadict["url"]
                method = datadict["method"]
                entry = method + ' ' + url
                calls.append(entry)
    total_calls = len(calls)
    return total_calls, Counter(calls)

# Copy the content of access.log to access.log_prev
def update_prev_file():
    open(prev_file, "w").writelines([l for l in open(access_log_file).readlines()])


def main():

    total = 0

    '''
    Check if prev file doesn't exist , then write access.log file content to it(for the initial execution) , and process the file .
    if the previous file exist :- 
        1) Check if the file access.log file change by comparing the content with previous 
            1.1) then process only the difference lines
            1.2) copy the access.log content to previous for the next comparision .
        2) otherwise , skip the calculation - nothing changed .  
    '''
    if not os.path.isfile(prev_file):
        open(prev_file, "w").writelines([l for l in open(access_log_file).readlines()])
        total, counters = get_calls_uniq_counter(prev_file)
    else:
        with open(access_log_file, 'r') as file1:
            with open(prev_file, 'r') as file2:
                difference = set(file1).difference(file2)
        difference.discard('\n')

        # examine if the current access.log file difference than previous content , then  process only the lines
        if len(difference) != 0:
            with open(prev_file, 'w') as file_out:
                for line in difference:
                    file_out.write(line)
            # call to get_calls_uniq_counter() method - to collect the uniq counters
            total, counters = get_calls_uniq_counter(prev_file)


    # Print the summary calls
    print("Total of %d calls since last interval" % (total))
    if total != 0:
        print("Uniqe calls:")
        for k in counters:
            print(k + ": " + str(counters[k]))

    # update the prev-access-log with the current file content
    update_prev_file()

if __name__ == '__main__':
    main()