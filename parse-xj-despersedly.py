import sys, os

PARSER = "/home/raphael/apps/stanford-parser/dep.berkeley.sh"
WORKDIR = "depparsing.tmp"
LINES_PER_PART = 10000


if len(sys.argv) != 3:
  print "python parse-berkeley-to-dep-despersedly.py [Berkeley Result] [Output File]"
  sys.exit()

if not os.path.exists(WORKDIR):
  os.mkdir(WORKDIR)

# Dispersion.
print "[MAIN] Dispersing ..."
linesResult = open(sys.argv[1]).xreadlines()
pathOutput = sys.argv[2]

nLine = 0
maxParts = 0
nPart = 0
filePart = None

for line in linesResult:
  nLine += 1
  if nLine % LINES_PER_PART == 1:
    nPart += 1
    maxParts += 1
    filePart = open("%s/part.%d" % (WORKDIR, nPart), "w")
  filePart.write(line)

# Parsing.
print "[MAIN] Parsing ..."
for nPart in range(1, maxParts + 1):
  pathPart = "%s/part.%d" % (WORKDIR, nPart)
  pathParsed = "%s/parsed.%d" % (WORKDIR, nPart)
  command = "%s %s > %s" % (PARSER, pathPart, pathParsed)
  print command
  os.system(command)

# Merging.
print "[MAIN] Merging ..."
fileOutput = open(pathOutput, "w")
for nPart in range(1, maxParts + 1):
  pathParsed = "%s/parsed.%d" % (WORKDIR, nPart)
  fileOutput.write(open(pathParsed).read())

