import sys

if len(sys.argv) != 2:
  print """
Space Remover
python space-remove.py [filename] > [output-file]
  """
  sys.exit()

file = sys.argv[1]
lines = open(file).xreadlines();

for line in lines:
  print line.replace(" ",""),

