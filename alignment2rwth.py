import sys,os

if len(sys.argv)!=2:
	print "Convert Alignment file from Moses to RWTH Format -Raphael 2012.1"
	print "Usage:"
	print "python alignment2rwth.py [file-of-alignment]"
	sys.exit()
	
path_input = sys.argv[1]
path_output = "%s.rwth" % path_input

if not os.path.exists(path_input) :
	print "File can not be found"
	sys.exit()
	
lines = open(path_input).xreadlines()
foutput = open(path_output,"w")

i = 0
for line in lines:
	foutput.write("SENT: %d\n" % i)
	pairs = line.replace("\n","").split(" ")
	for pair in pairs:
		foutput.write("S %s\n" % pair.replace("-"," "))
	foutput.write("\n")
	i = i + 1
	if (i % 1000) == 0:
		print "[Sent] %d" % i

foutput.close()
	