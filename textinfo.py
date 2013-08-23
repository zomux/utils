import os,sys

if len(sys.argv)<2:
  # textinfo.py
  print "Usage:"
  sys.exit()

command = sys.argv[1]

if command == "-countwords":
  mapWordCount = {}
  file = sys.argv[2]
  lines = open(file).xreadlines()
  for line in lines:
    words = line.strip().split(" ")
    for word in words:
      mapWordCount.setdefault(word,0)
      mapWordCount[word] += 1
    
  words = mapWordCount.keys()
  words.sort(key=lambda x:mapWordCount[x],reverse=True)
  print words[:100]
elif command == "-countnoaligns":
  # textinfo.py corpus alignmentfile
  print "textinfo.py corpus alignmentfile"
  # count for no align hit
  mapWordCount = {}
  corpus = sys.argv[2]
  alignment_file = sys.argv[3]
  lines_corpus = open(corpus).readlines()
  lines_alignment = open(alignment_file).readlines()
  for iLine in range(len(lines_corpus)):
    aligned_srcs = []
    aligns = lines_alignment[iLine].strip().split(" ")
    for align in aligns:
      aligned_srcs.append(int(align.split("-")[0]))
    words = lines_corpus[iLine].strip().split(" ")
    for iWord,word in enumerate(words):
      if iWord not in aligned_srcs:
        mapWordCount.setdefault(word,0)
        mapWordCount[word] += 1
  words = mapWordCount.keys()
  words.sort(key=lambda x:mapWordCount[x],reverse=True)
  print "\n".join([w+" "+str(mapWordCount[w]) for w in words[:100]])
elif command == "-countphrases":
  # textinfo -countwordpairs corpus
  corpus = sys.argv[2]
  n = 2
  mapPhraseCount = {}
  lines_corpus = open(corpus).readlines()
  for line in lines_corpus:
    words = line.strip().split(" ")
    for i in range(0,len(words)-n+1):
      phrase = " ".join(words[i:i+n])
      mapPhraseCount.setdefault(phrase,0)
      mapPhraseCount[phrase] += 1
  
  phrases = mapPhraseCount.keys()
  phrases.sort(key=lambda x:mapPhraseCount[x],reverse=True)
  print "\n".join([w+" "+str(mapPhraseCount[w]) for w in phrases[:100]])
    
  