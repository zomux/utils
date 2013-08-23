import sys,os

if len(sys.argv) != 3:
  print("Filter corpus and drop sents with sharp  -Raphael")
  print("Usage:")
  print("python filter-sharp.py [corpus-e] [corpus-f]")
  sys.exit()
  
path_input_f = sys.argv[2]
path_input_e = sys.argv[1]
path_output_f = "%s.nosharp" % path_input_f
path_output_e = "%s.nosharp" % path_input_e

#check for files
if not os.path.exists(path_input_f) or not os.path.exists(path_input_e): 
  print "Error , File can not be found."
  sys.exit()

print "Filter result will be saved in:"
print "%s and %s" % (path_output_f,path_output_e)
#read files
lines_f = open(path_input_f).readlines()
lines_e = open(path_input_e).readlines()
#check length
if len(lines_f) != len(lines_e):
  print "Incorresponding Length"
  sys.exit()

foutput_f = open(path_output_f,"w")
foutput_e = open(path_output_e,"w")
for i in range(0,len(lines_e)):
  line_e = lines_e[i]
  line_f = lines_f[i]
  if line_e.count('#')==0 and line_f.count("#")==0:
    foutput_e.write(line_e)
    foutput_f.write(line_f)

foutput_f.close()
foutput_e.close()

