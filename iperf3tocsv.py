#!/usr/bin/env python

"""
    Version: 1.1

    Author: Kirth Gersen
    Date created: 6/5/2016
    Date modified: 9/12/2016
    Python Version: 2.7

"""

from __future__ import print_function
import json
import sys
import csv

db = {}

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def main():
    global db
    """main program"""

    csv.register_dialect('iperf3log', delimiter=',', quoting=csv.QUOTE_MINIMAL)
    csvwriter = csv.writer(sys.stdout, 'iperf3log')

    if len(sys.argv) == 2:
        if (sys.argv[1] != "-h"):
            sys.exit("unknown option")
        else:
            csvwriter.writerow(["date", "ip", "localport", "remoteport", "duration", "protocol", "num_streams", "cookie", "sent", "sent_mbps", "rcvd", "rcvd_mbps", "totalsent", "totalreceived"])
            sys.exit(0)

    # accummulate volume per ip in a dict
    db = {}
    
    # highly specific json parser
    # assumes top { } pair are in single line

    jsonstr = ""
    i = 0
    m = False
    for line in sys.stdin:
        i += 1
        if line == "{\n":
            jsonstr = "{"
            #print("found open line %d",i)
            m = True
        elif line == "}\n":
            jsonstr += "}"
            #print("found close line %d",i)
            if m:
                process(jsonstr,csvwriter)
            m = False
            jsonstr = ""
        else:
            if m:
                jsonstr += line
            #else:
                #print("bogus at line %d = %s",i,line)

def process(js,csvwriter):
    global db
    #print(js)
    try:
        obj = json.loads(js)
    except:
        eprint("bad json")
        pass
        return False 
    try:
        # caveat: assumes multiple streams are all from same IP so we take the 1st one
        # todo: handle errors and missing elements
        ip = (obj["start"]["connected"][0]["remote_host"]).encode('ascii', 'ignore')
        local_port = obj["start"]["connected"][0]["local_port"]
        remote_port = obj["start"]["connected"][0]["remote_port"]

        sent = obj["end"]["sum_sent"]["bytes"]
        rcvd = obj["end"]["sum_received"]["bytes"]
        sent_speed = obj["end"]["sum_sent"]["bits_per_second"] / 1000 / 1000
        rcvd_speed = obj["end"]["sum_received"]["bits_per_second"] / 1000 / 1000
        

        reverse = obj["start"]["test_start"]["reverse"]
        time = (obj["start"]["timestamp"]["time"]).encode('ascii', 'ignore')
        cookie = (obj["start"]["cookie"]).encode('ascii', 'ignore')
        protocol = (obj["start"]["test_start"]["protocol"]).encode('ascii', 'ignore')
        duration = obj["start"]["test_start"]["duration"]
        num_streams = obj["start"]["test_start"]["num_streams"]
        if reverse not in [0, 1]:
            sys.exit("unknown reverse")

        s = 0
        r = 0
        if ip in db:
            (s, r) = db[ip]

        if reverse == 0:
            r += rcvd
            sent = 0
            sent_speed = 0
        else:
            s += sent
            rcvd = 0
            rcvd_speed = 0

        db[ip] = (s, r)

        csvwriter.writerow([time, ip, local_port, remote_port, duration, protocol, num_streams, cookie, sent, sent_speed, rcvd, rcvd_speed, s, r])
        return True
    except:
       eprint("error or bogus test:", sys.exc_info()[0])
       pass
       return False

def dumpdb(database):
    """ dump db to text """
    for i in database:
        (s, r) = database[i]
        print("%s, %d , %d " % (i, s, r))

if __name__ == '__main__':
    main()
