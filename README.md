# iperf3tocsv

 - set iperf3 server to ouput in json (-J)
 - parse the json for each test
 - sum usage per IP
 - output a log line
 
usage:

    iperf3 -s -J | python -u iperf3tocsv.py

options:

`python iperf3tocsv.py -h` will display the column headers and exit

