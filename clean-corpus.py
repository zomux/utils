import sys,os

def cmd(cmd):
    print cmd
    os.system(cmd)

class Cleaner(object):
  src, tgt = None, None
  sourceEns, sourceJas, sourceAlignments, sourceCFGs, sourceDEPs = None, None, None, None, None
  fTargetEn, fTargetJa, fTargetAlignment, fTargetCFG, fTargetDEP = None, None, None, None, None

  def __init__(self, src, tgt):
    self.src = src
    self.tgt = tgt
    cmd("mkdir %s" % tgt)
    cmd("cp %s/lex.f2e %s/lex.f2e" % (src,tgt))
    cmd("cp %s/lex.e2f %s/lex.e2f" % (src,tgt))
    self.load()

  def load(self):
    src = self.src
    tgt = self.tgt
    if os.path.exists("%s/aligned.grow-diag-final-and" % src):
      self.sourceAlignments = open("%s/aligned.grow-diag-final-and" % src).readlines()
      self.fTargetAlignment = open("%s/aligned.grow-diag-final-and" % tgt, "w")
    if os.path.exists("%s/data.en" % src):
      self.sourceEns = open("%s/data.en" % src).readlines()
      self.fTargetEn = open("%s/data.en" % tgt, "w")
    if os.path.exists("%s/data.ja" % src):
      self.sourceJas = open("%s/data.ja" % src).readlines()
      self.fTargetJa = open("%s/data.ja" % tgt, "w")
    if os.path.exists("%s/data.en.tree" % src):
      self.sourceCFGs = open("%s/data.en.tree" % src).readlines()
      self.fTargetCFG = open("%s/data.en.tree" % tgt, "w")
    if os.path.exists("%s/data.en.dep" % src):
      self.sourceDEPs = open("%s/data.en.dep" % src).read().split("\n\n")
      self.fTargetDEP = open("%s/data.en.dep" % tgt, "w")

  def process(self):
    for nLine in xrange(len(self.sourceEns)):
      wordCountEn = self.sourceEns[nLine].count(" ") + 1
      wordCountJa = self.sourceJas[nLine].count(" ") + 1
      if wordCountEn > 40 or wordCountJa > 40:
        continue
      self.saveToTarget(nLine)

  def saveToTarget(self, nLine):
    if self.fTargetAlignment:
      self.fTargetAlignment.write(self.sourceAlignments[nLine])
    if self.fTargetEn:
      self.fTargetEn.write(self.sourceEns[nLine])
    if self.fTargetJa:
      self.fTargetJa.write(self.sourceJas[nLine])
    if self.fTargetCFG:
      self.fTargetCFG.write(self.sourceCFGs[nLine])
    if self.fTargetDEP:
      self.fTargetDEP.write(self.sourceDEPs[nLine] + "\n\n")

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "Automatically clean Corpus"
    print "python cut-corpus.py source-folder target-folder"
    sys.exit()
  _,src,tgt = sys.argv
  print "Begin to clean, %s -> %s" % (src, tgt)
  cleaner = Cleaner(src, tgt)
  cleaner.process()


