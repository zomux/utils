#!python
import os, sys

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print "python count-line-by-length.py [file] [min-length]"
    raise SystemExit
  _, filename, minLength = sys.argv
  minLength = int(minLength)
  counter = 0
  for line in open(filename).xreadlines():
    if line.strip().count(" ") + 1 >= minLength:
      counter += 1

  print counter