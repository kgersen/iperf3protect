# iperf3protect

draft WIP

 - set iperf3 server to ouput in json (-J)
 - parse the json for each test
 - sum usage per IP
 - output a log line
 
1st draft: convert result to cvs

usage:

iperf3 -s -J | python iperf3tocsv.py


 
