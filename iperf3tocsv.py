import json, sys
from splitstream import splitfile

# this will yield each test as a parsed json
objs = (json.loads(jsonstr) for jsonstr in splitfile(sys.stdin, format="json", bufsize=1))
print "ip,sent,received"
for obj in objs:
    # caveat: assumes multiple streams are all from same IP so we take the 1st one
    print "%s, %d, %d" % (obj["start"]["connected"][0]["remote_host"], obj["end"]["sum_sent"]["bytes"], obj["end"]["sum_received"]["bytes"])

