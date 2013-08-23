import sys

if len(sys.argv) != 2:
  print("Filter rule table with invalid '|'  -Raphael")
  print("Usage:")
  print("python filter-rule-table.py [rule-table]")
  sys.exit()
path_input = sys.argv[1]
path_output = "%s.filtered" % path_input
print("Write filtered rule table into:",path_output)
fnew = open(path_output,'w')
lines = open(path_input).xreadlines()
for line in lines:
  if line.count('|') != 12:
    print '[E]',line
  else:
    fnew.write(line)

fnew.close()



