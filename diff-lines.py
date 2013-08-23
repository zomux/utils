import os,sys

if len(sys.argv) != 3:
  print "python diff-lines.py [file1] [file2]"
  sys.exit()
  
file1 = sys.argv[1]
file2 = sys.argv[2]

f1 = open(file1)
f2 = open(file2)

curLine = 1

line1 = f1.readline()
line2 = f2.readline()

while line1 or line2:
  if line1 != line2:
    print "first diff line found: %d" % curLine
    break
  line1 = f1.readline()
  line2 = f2.readline()
  curLine += 1
  
