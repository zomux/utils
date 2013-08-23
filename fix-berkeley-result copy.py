import os,sys

class GeneralTree:
  """
  A class represents gernal tree structure.
  """
  nodes = None
  mapParent = None
  mapChildren = None
  root = None

  def __init__(self):
    """
    Initialize members.
    """
    self.nodes, self.mapParent, self.mapChildren = {}, {}, {}

  def node(self, id):
    """
    Get the node by given node id.
    """
    return self.nodes[id] if id in self.nodes else None

  def parent(self, id):
    """
    Get the id of parent node.
    """
    return self.mapParent[id] if id in self.mapParent else None

  def children(self, id):
    """
    Get the id of parent node.
    """
    return self.mapChildren[id] if id in self.mapChildren else []

  def buildChildrenMap(self):
    """
    Automatically build map of chilren by map of parents.
    """
    self.mapChildren = {}
    for nodeId in self.mapParent:
      parentId = self.mapParent[nodeId]
      self.mapChildren.setdefault(parentId, []).append(nodeId)

class PCFGTree:
  """
  A class represents PCFG tree.
  """
  tokens = None
  tree = None


  def __init__(self, textPCFG):
    """
    Initialize.
    """
    self.tokens = []
    self.tree = GeneralTree()
    self.parsePCFG(textPCFG)
    self.tree.buildChildrenMap()

  def parsePCFG(self, textPCFG):
    """
    Build the tree with PCFG result.
    """
    if textPCFG.startswith("( "):
      textPCFG = textPCFG[2:]
    if textPCFG.endswith(" )"):
      textPCFG = textPCFG[:-2]
    textPCFG = textPCFG.replace("(","( ").replace(")"," )").replace("  "," ")
    # Begin parsing.
    nodeId = 1
    depth = 0
    branchStack = []
    currentNode = None
    currentNodeId = None
    for part in textPCFG.split(" "):
      if part == "(":
        if not currentNode:
          continue
        currentNodeId = nodeId
        nodeId += 1
        self.tree.nodes[currentNodeId] = currentNode
        if branchStack:
          self.tree.mapParent[currentNodeId] = branchStack[-1]
        else:
          self.tree.root = currentNodeId
        branchStack.append(currentNodeId)
        # Clear stage.
        currentNodeId = None
        currentNode = None
      elif part == ")":
        if branchStack:
          currentNodeId = branchStack.pop()
      else:
        if not currentNode:
          currentNode = (part, None)
        else:
          tag, _ = currentNode
          # For terminal it should be (tag, token id)
          currentNode = (tag, len(self.tokens) + 1)
          self.tokens.append((tag, part))
          # Record Terminal Node.
          currentNodeId = nodeId
          nodeId += 1
          self.tree.nodes[currentNodeId] = currentNode
          if branchStack:
            self.tree.mapParent[currentNodeId] = branchStack[-1]
          else:
            self.tree.root = currentNodeId
          branchStack.append(currentNodeId)
          # Clear stage.
          currentNode = None


if __name__ == "__main__":
  # Fix berkeley results.
  if len(sys.argv) < 3:
    print "python filter-berkley-result.py [result-file] [source file] [files-also-filter] ..."
    print "example:"
    print "python filter-berkley-result.py data.en.tree data.en data.ja aligned.grow-diag-final-and"
    sys.exit()

  pathSource = sys.argv[2]
  pathTree = sys.argv[1]
  pathOtherFiles = sys.argv[3:]

  fileSource = open(pathSource)
  fileTree = open(pathTree)

  # Build map for sentence to tree.
  mapSentenceTree = {}

  linesTree = fileTree.xreadlines()
  n = 0
  for lineTree in linesTree:
    if n % 10000 == 0:
      print n/10000,
      sys.stdout.flush()
    lineTree = lineTree.strip()
    if lineTree == "(())":
      continue
    cfg = PCFGTree(lineTree)
    tokens = map(lambda x: x[1], cfg.tokens)
    sentence = " ".join(tokens)
    mapSentenceTree[hash(sentence)] = lineTree
    n += 1
  print ""
  # Check each source sentence.
  pathNewSource = "%s.filtered" % pathSource
  pathNewTree = "%s.filtered" % pathTree
  pathOtherNewFiles = ["%s.filtered" % p for p in pathOtherFiles]

  fileNewSource = open(pathNewSource, "w")
  fileNewTree = open(pathNewTree, "w")
  otherFiles = [open(f) for f in pathOtherFiles]
  otherNewFiles = [open(f, "w") for f in pathOtherNewFiles]


  errors = 0
  n = 0
  lineSource = fileSource.readline()
  while lineSource:
    if n % 10000 == 0:
      print n/10000,
      sys.stdout.flush()
    lineSource = lineSource.strip()
    k = hash(lineSource)
    if k in mapSentenceTree:
      # Tree found.
      fileNewSource.write(lineSource + "\n")
      lineTree = mapSentenceTree[k]
      fileNewTree.write(lineTree + "\n")
      for n, otherFile in enumerate(otherFiles):
        line = otherFile.readline()
        otherNewFiles[n].write(line)

    else:
      for n, otherFile in enumerate(otherFiles):
        line = otherFile.readline()
      errors += 1
    n += 1
    lineSource = fileSource.readline()

  print ""
  print "errors found:", errors















