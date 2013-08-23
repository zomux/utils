import sys,os

if len(sys.argv) != 3:
  print("Filter corpus with limited length  -Raphael 2012.2")
  print("Usage:")
  print("python filter-with-length.py [corpus] [length]")
  sys.exit()
  
path_input = sys.argv[1]
limited_length = int(sys.argv[2])
path_output = "%s.limited" % path_input

if not os.path.exists(path_input):
  print "Cannot found input file , fuck you"
  sys.exit()
  
foutput = open(path_output,"w")
lines = open(path_input).xreadlines()
for line in lines:
  if line.count(' ') >= limited_length:
    print "[F]",line.count(" ")+1,line
  else:
    foutput.write(line)
    
foutput.close()




