#!/usr/bin/python
import sys

def ez():
  if len(sys.argv) < 3:
    print '<usage> ml_easy_peer_grade [YOUR_ID] [YOUR_LAST_NAME] [nth_LAST_NAME]*'
  else:
    args = sys.argv[1:]
    f = open('{}.txt'.format(args[0]), 'w')
    s = "{0[0]} {0[1]}\n".format(args)
    last_names = args[2:]
    for name in last_names:
      s += "{} 1\n".format(name)
    f.write(s)
    f.close() 
