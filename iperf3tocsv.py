import json, sys
from splitstream import splitfile

# debug: 300MB and 400MB
# todo: get these from cmd line parameters
gMaxSend = 300*1000*1000
gMaxReceive = 400*1000*1000

# accummulate volume per ip in a dict
db = {}
# this will yield each test as a parsed json
objs = (json.loads(jsonstr) for jsonstr in splitfile(sys.stdin, format="json", bufsize=1))
print "ip,sent,received,direction"
for obj in objs:
    # caveat: assumes multiple streams are all from same IP so we take the 1st one
    ip   = obj["start"]["connected"][0]["remote_host"]
    sent = obj["end"]["sum_sent"]["bytes"]
    rcvd = obj["end"]["sum_received"]["bytes"]
    reverse = obj["start"]["test_start"]["reverse"]
    if reverse not in [0,1]:
        print 'panic: unknown "reverse"'
    print "  %s, %d, %d, %d" % (ip, sent , rcvd, reverse)
    s = 0
    r = 0
    if ip in db:
        (s,r) = db[ip]

    if reverse == 0:
        r+=rcvd
    else:
        s+=sent

    db[ip]=(s,r)
    
    if (s>gMaxSend):
        print "%s is over the send cap with %d" % (ip,s)
    if (r>gMaxReceive):
        print "%s is over the receive cap with %d" % (ip,r)

    for i in db:
       (s,r)=db[i]
       print "%s, %d , %d " % (i,s,r)
