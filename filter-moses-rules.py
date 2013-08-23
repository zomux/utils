import os,sys

if len(sys.argv) != 2:
  print "python filter-moses-rules.py [moses-rule-table]"
  exit()

_, path = sys.argv

lines = open(path).readlines()

for line in lines:
  line = line.strip()
  if not line:
    continue
  parts = line.split(" ||| ")
  if "|" in parts[0]:
    continue
  print line