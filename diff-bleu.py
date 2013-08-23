import sys, os

if len(sys.argv) != 4:
  print "python diff-bleu.py [result1] [result2] [reference]"
  raise SystemExit

_, pathResult1, pathResult2 , pathRef = sys.argv

def listLineBleu(pathResult, pathRef):
  resultLineBleus = os.popen("ruby ~/apps/bleu_kit/line_bleu.rb %s %s" % (pathResult, pathRef)).read().strip()
  lineBleus = resultLineBleus.split("\n")
  return [float(l.split("\t")[0]) for l in lineBleus]

def readFileLines(filename):
	lines = open(filename).readlines()
	return lines


listBleus1 = listLineBleu(pathResult1, pathRef)
listBleus2 = listLineBleu(pathResult2, pathRef)

pathSrc = pathRef.replace(".ja", ".en").replace(".ref", ".src")

resLines1, resLines2, refLines, srcLines = map(readFileLines, [pathResult1, pathResult2, pathRef, pathSrc])

confLines = [""]*len(listBleus1)
pathConf = "data.en.tree.conf"
if os.path.exists(pathConf):
	confLines = [float(x.split("\t")[0]) for x in readFileLines(pathConf)]

sortedLineNumbers = range(len(listBleus1))

sortedLineNumbers.sort(key=lambda x:listBleus2[x] - listBleus1[x], reverse=True)

# Output
for lineNumber in sortedLineNumbers:
	length = srcLines[lineNumber].count(" ") + 1
	print "[%d| %f - %f = %f, C%s] %s" % (lineNumber, listBleus2[lineNumber], listBleus1[lineNumber], listBleus2[lineNumber] - listBleus1[lineNumber], confLines[lineNumber]/length ,srcLines[lineNumber].strip())
	print "[REF]", refLines[lineNumber].strip()
	print "[RS2]", resLines2[lineNumber].strip()
	print "[RS1]", resLines1[lineNumber].strip()
	print ""
