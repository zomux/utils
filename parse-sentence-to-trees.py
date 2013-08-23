import sys, os, tempfile

if len(sys.argv) != 2:
  print "python parse-sentence-to-trees.py [sentence]"

def execute(cmd):
  print cmd
  os.system(cmd)

_, sentence = sys.argv

sentence = sentence.strip()

_, pathText = tempfile.mkstemp()
_, pathCFG = tempfile.mkstemp()
_, pathDep = tempfile.mkstemp()

open(pathText, "w").write(sentence)

execute("/home/raphael/apps/berkley/parse.sh < %s > %s" % (pathText, pathCFG))

execute("/home/raphael/apps/stanford-parser/dep.berkeley.sh %s > %s" % (pathCFG, pathDep))

print "--- CFG ---"
print open(pathCFG).read().strip()

print "--- DEP ---"
print open(pathDep).read().strip()
