from facecom import *
import sys
import pprint

if len(sys.argv) < 3:
    print "Usage: %s api_key api_secret" % (sys.argv[0],)
    sys.exit(0)

images='http://sphotos.ak.fbcdn.net/hphotos-ak-snc3/hs356.snc3/29413_1451698097591_1387417105_31223384_6233008_n.jpg'

h = FaceRestClient(sys.argv[1], sys.argv[2], format='json')
pprint.pprint(h.faces_detect(images))

h = FaceRestClient(sys.argv[1], sys.argv[2], format='xml')
pprint.pprint(h.faces_detect(images).toxml())
