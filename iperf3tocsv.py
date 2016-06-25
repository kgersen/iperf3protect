#!/usr/bin/env python

"""
    Version: 1.0

    Author: Kirth Gersen
    Date created: 6/5/2016
    Date last modified: 6/7/2016
    Python Version: 2.7

"""

import json
import sys
import csv
# todo: get ride of splitfile
from splitstream import splitfile



def main():
    """main program"""

    csv.register_dialect('iperf3log', delimiter=',', quoting=csv.QUOTE_MINIMAL)

    csvwriter = csv.writer(sys.stdout, 'iperf3log')

    # accummulate volume per ip in a dict
    db = {}
    # this will yield each test as a parsed json
    objs = (json.loads(jsonstr) for jsonstr in splitfile(sys.stdin, format="json", bufsize=1))

    csvwriter.writerow(["date", "ip", "localport", "remoteport", "duration", "protocol", "num_streams", "cookie", "sent", "sent_mbps", "rcvd", "rcvd_mbps", "totalsent", "totalreceived"])
    for obj in objs:
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
    # for obj
    sys.exit(0)


def dumpdb(database):
    """ dump db to text """
    for i in database:
        (s, r) = database[i]
        print("%s, %d , %d " % (i, s, r))

if __name__ == '__main__':
    main()
