import sys,os

if len(sys.argv) < 2:
  print "Cluster Text Processer  -Raphael"
  print "Usage:"
  print "python ctext.py -c [corpus]  #count the corpus"
  print "python ctext.py -i [begin] [length] [corpus]  #cut the corpus"
  sys.exit()
  
command = sys.argv[1]

if command == "-c":
  if len(sys.argv) != 3:
    print "CTEXT: argument error"
    sys.exit()
  corpus = sys.argv[2]
  if not os.path.exists(corpus) :
    print "CTEXT: file not exists"
    sys.exit()
  data = open(corpus).read()
  list_clusters = data.split("\n\n")
  count_list = len(list_clusters)
  if list_clusters[-1] == "":
    count_list = count_list - 1
  print count_list

elif command == "-i":
  if len(sys.argv) != 5:
    print "CTEXT: argument error"
    sys.exit()
  corpus = sys.argv[4]
  begin =int(sys.argv[2])
  length = int(sys.argv[3])
  if not os.path.exists(corpus) :
    print "CTEXT: file not exists"
    sys.exit()
  data = open(corpus).read()
  list_clusters = data.split("\n\n")
  list_clusters = list_clusters[begin:begin+length]
  text_output = "\n\n".join(list_clusters)
  print text_output