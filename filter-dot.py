import sys,os

if len(sys.argv) != 2:
  print("Filter corpus and drop extenal dot  -Raphael")
  print("Usage:")
  print("python filter-dot.py [corpus]")
  sys.exit()
  
path_input = sys.argv[1]

#check for files
if not os.path.exists(path_input): 
  print >> sys.stderr, "Error , File can not be found."
  sys.exit()

#read files
lines = open(path_input).xreadlines()

for line in lines:
  line = line.strip()

  line = line.replace(" . "," <DOT> ")
  line = line.replace("fig <DOT>","FIGDOT")
  line = line.replace("figs <DOT>","FIGSDOT")
  line = line.replace("no <DOT>","NODOT")
  line = line.replace("<DOT> . <DOT>","DOTDOTDOT")
  print line

