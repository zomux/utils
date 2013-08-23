import sys, os

if len(sys.argv) != 3:
  print "python detail-bleu.py [result] [reference]"
  raise SystemExit

_, pathResult, pathRef = sys.argv

def listLineBleu(pathResult, pathRef):
  resultLineBleus = os.popen("ruby ~/apps/bleu_kit/line_bleu.rb %s %s" % (pathResult, pathRef)).read().strip()
  lineBleus = resultLineBleus.split("\n")
  return [float(l.split("\t")[0]) for l in lineBleus]



listBleus = listLineBleu(pathResult, pathRef)

# Count zero bleu lines.
print "Bleu=0 lines:", listBleus.count(0.0)

pathMoses = pathResult.replace("gentile.", "moses.")
if "moses" not in pathResult and os.path.exists(pathMoses):
  listMosesBleus = listLineBleu(pathMoses, pathRef)

# Count for ranged length.

pathEn = pathRef.replace(".ja", ".en")
linesEn = open(pathEn).read().strip().split("\n")
mapLengthBleuSum, mapLengthCount = {}, {}
for iLine, lineEn in enumerate(linesEn):
  if lineEn.count(" ") < 10:
    rangedLength = 10
  elif lineEn.count(" ") < 15:
    rangedLength = 15
  elif lineEn.count(" ") < 20:
    rangedLength = 20
  elif lineEn.count(" ") < 25:
    rangedLength = 25
  elif lineEn.count(" ") < 30:
    rangedLength = 30
  elif lineEn.count(" ") < 35:
    rangedLength = 35
  elif lineEn.count(" ") < 40:
    rangedLength = 40

  elif lineEn.count(" ") < 43:
    rangedLength = 43
  elif lineEn.count(" ") < 44:
    rangedLength = 44
  else:
    rangedLength = 45
  mapLengthBleuSum.setdefault(rangedLength, 0)
  mapLengthCount.setdefault(rangedLength, 0)
  mapLengthBleuSum[rangedLength] += listBleus[iLine] - listMosesBleus[iLine]
  mapLengthCount[rangedLength] += 1

for rangedLength in sorted(mapLengthBleuSum.keys()):
  print "Bleu with ranged length %d:" % rangedLength, float(mapLengthBleuSum[rangedLength]/mapLengthCount[rangedLength]), "Count:", mapLengthCount[rangedLength]

# Compare with moses.
pathMoses = pathResult.replace("gentile.", "moses.")
if "moses" not in pathResult and os.path.exists(pathMoses):
  listMosesBleus = listLineBleu(pathMoses, pathRef)
  improvedLineNumbers = [x for x in range(len(listBleus)) if listBleus[x] > (listMosesBleus[x]+0.05)]
  print "Better than Moses:", len(improvedLineNumbers)
  print "---"
  linesGentile = open(pathResult).read().split("\n")
  for improvedLineNumber in improvedLineNumbers:
    continue
    print linesGentile[improvedLineNumber]

# Compare with gentile.
pathMoses = pathResult.replace("moses.", "gentile.")
if "gentile" not in pathResult and os.path.exists(pathMoses):
  listMosesBleus = listLineBleu(pathMoses, pathRef)
  improvedLineNumbers = [x for x in range(len(listBleus)) if listBleus[x] > (listMosesBleus[x]+0.05)]
  print "Better than Gentile:", len(improvedLineNumbers)
  print "---"