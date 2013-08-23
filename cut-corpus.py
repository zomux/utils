import sys,os

if len(sys.argv) != 5:
    print "Automatically Cut Corpus"
    print "python cut-corpus.py source-folder target-folder begin length"
    sys.exit()

def cmd(cmd):
    print cmd
    os.system(cmd)

_,src,tgt,begin,length = sys.argv

begin = int(begin)
length = int(length)
end = begin + length

cmd("mkdir %s" % tgt)
cmd("head -n %d %s/aligned.grow-diag-final-and | tail -n %d > %s/aligned.grow-diag-final-and" % (end, src, length, tgt))
cmd("head -n %d %s/data.en | tail -n %d > %s/data.en" % (end, src, length, tgt))
cmd("head -n %d %s/data.ja | tail -n %d > %s/data.ja" % (end, src, length, tgt))
if os.path.exists("%s/data.en.tagdep" % src):
  cmd("python ~/tools/ctext.py -i %d %d %s/data.en.tagdep > %s/data.en.tagdep" % (begin*2, length*2, src, tgt))
if os.path.exists("%s/data.en.tree" % src):
  cmd("head -n %d %s/data.en.tree | tail -n %d > %s/data.en.tree" % (end, src, length, tgt))
if os.path.exists("%s/data.en.dep" % src):
  cmd("python ~/tools/ctext.py -i %d %d %s/data.en.dep > %s/data.en.dep" % (begin, length, src, tgt))
cmd("cp %s/lex.f2e %s/lex.f2e" % (src,tgt))
cmd("cp %s/lex.e2f %s/lex.e2f" % (src,tgt))
