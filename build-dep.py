# coding:utf-8
"""
Build dep for large corpus 

use multiple process on running stanford parser 

                               - Raphael 2012.2
"""

# configuration
file_input = "data.en"
file_output = file_input + ".tagdep"
command = "/home/raphael/apps/stanford-parser/tagdep.sh"
limit_threads = 5
tmpdir = "tmp.builddep"
# Lib
import sys,os,urllib2,urllib,re,time,threading

# Global Vars
global_end = False
global_exits = 0
# Global Locks
# Custom Functions
# Thread Process
def thread_proc(id):
  global global_end,global_exits
  global file_input,file_output,command,tmpdir
  # Thread Process pre runing
  path_input = "%s/input.%d" % (tmpdir,id)
  path_output = "%s/output.%d" % (tmpdir,id)
  os.system("%s %s > %s" % (command,path_input,path_output)) 
  # end
  while True:
    # Thread Process Begin
    break
    # Thread Process End
  global_exits += 1
  print "[%d] Thread Exited" % id
  return

# main process start
print "Main Thread started"
# main process pre running code
if os.path.exists(tmpdir):
  os.system("rm -r %s" % tmpdir)

os.mkdir(tmpdir)

data = open(file_input).readlines()
len_data = len(data)
print "[M]","%d lines need to process" % len_data
len_block = len_data/limit_threads

for i in range(limit_threads):
  tmpfile = "%s/input.%d" % (tmpdir,i)
  open(tmpfile,"w").write("".join(data[len_block*i:len_block*i+len_block]))

global_end = True
# end of  process pre running 
# Welcome
print "Loading processes ... "
# Fork Process
for i in range(0,limit_threads):
  thProcess = threading.Thread(target=thread_proc,args=(i,))
  thProcess.start()

while True:
  # maintain pools
  

  # end maintain pools
  if global_end and global_exits >= limit_threads:
    print "[M]","Main Thread Exiting"
    break
  time.sleep(1)

# code after all over
foutput = open(file_output,"w")
for i in range(limit_threads):
  tmpfile = "%s/output.%d" % (tmpdir,i)
  foutput.write( open(tmpfile).read() )
foutput.close()

# main process end
print "[M]","Main Thread Exited"


