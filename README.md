# iperf3protect
prevent public iperf3 server abuse - WIP

draft WIP

we want to block some IP when they abuse an iperf3 server.
method:
 - set iperf3 server to ouput in json (-J)
 - parse the json for each test
 - todo: sum usage per IP
 - todo: block abusers using iptables
 
1st draft: convert result to cvs

usage:

iperf3 -s -J | python iperf3tocsv.py
 
