import sys,os,re

if len(sys.argv) != 2:
  print "python split-brackets.py [file]"
  sys.exit()

symbolsToProcess = ["<", ">","(",")","[","]"]

file = sys.argv[1]
lines = open(file).xreadlines()
for line in lines:
  line = line.strip()
  if not line:
    continue
  for symbol in symbolsToProcess:
    symbolWithSpace = " %s " % symbol
    if symbol in line and symbolWithSpace not in line:
      line = line.replace(symbol, symbolWithSpace)
  line = line.strip().replace("  ", " ")
  print line
  
