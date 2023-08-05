#!/usr/bin/python
import sys

def ez():
  if len(sys.argv) != 6:
    print '<usage> ml_easy_peer_grade [YOUR_ID] [YOUR_LAST_NAME] [LAST_NAME_1] [LAST_NAME_2] [LAST_NAME_3]'
  else:
    args = sys.argv[1:]
    f = open('{}.txt'.format(args[0]), 'w')
    s = "{0[0]} {0[1]}\n{0[2]} 5\n{0[3]} 5\n{0[4]} 5\n".format(args)
    f.write(s)
    f.close() 
