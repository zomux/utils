import sys,os

if len(sys.argv)!=2 :
  print "Text Untokenizer --Raphael 2012.1"
  print "Usage:"
  print "python untokenizer.py [text]"
  sys.exit()

path_text = sys.argv[1]
if not os.path.exists( path_text ):
  print "File not exists."
  sys.exit()

path_output = path_text + ".raw"
lines = open(path_text).xreadlines()
foutput = open(path_output,'w')

for line in lines:
  line = line.replace("\r","").replace("\n","")
  list_tokens = line.split(" ")
  line_output = "".join(list_tokens)
  foutput.write(line_output+"\n")

foutput.close()
