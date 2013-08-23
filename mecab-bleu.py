import sys, os

if len(sys.argv) != 3:
  print "python chasen-bleu.py [result] [reference]"
  raise SystemExit

def rebuild_corpus(path, cate):
  # Remove spaces.
  print "[REBUILD]", path
  text = open(path).read().replace(" ","")
  open("/tmp/chasen-bleu.tmp.%s.nospace" % cate, "w").write(text)
  os.system('cat /tmp/chasen-bleu.tmp.%s.nospace | nkf -e | mecab -O wakati | nkf -w > /tmp/chasen-bleu.tmp.%s' % (cate, cate))
  print "[REBUILD]", '/tmp/chasen-bleu.tmp.%s' % cate
  return '/tmp/chasen-bleu.tmp.%s' % cate

_, pathResult, pathRef = sys.argv

pathResult = rebuild_corpus(pathResult, "res")
pathRef = rebuild_corpus(pathRef, "ref")

finalCommand = "ruby ~/apps/bleu_kit/doc_bleu.rb %s %s" % (pathResult, pathRef)
print finalCommand
os.system(finalCommand)
