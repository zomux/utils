#Build jane.config.final
#from jane.config and lambda.final
#-Raphael 2012.1

import sys,os
import ConfigParser

if len(sys.argv)!=2:
	print "jane.config.final builder -Raphael 2012.1"
	print "Usage:"
	print "python build-jane-final.py [TESTFILE]"
	sys.exit()
	
path_testfile = sys.argv[1]
path_config = "jane.config"
path_lambda = "lambda.final"
realpath_template = "/home/raphael/tools/build-jane-final.template"
if not os.path.exists(path_testfile) or not os.path.exists(path_config) or not os.path.exists(path_lambda):
	print "one file of [test,jane.config,lambda.final] not found"
	sys.exit()
	

ini = ConfigParser.SafeConfigParser()
ini.read(path_config)
path_lm = ini.get("Jane.CubeGrow.LM","file")
path_rule = ini.get("Jane.CubeGrow.rules","file")

text_lambda = open(path_lambda).read()
text_lambda = text_lambda.replace(" "," = ")

text_output = open(realpath_template).read()
text_output = text_output.replace("<LMFILE>",path_lm)
text_output = text_output.replace("<RULEFILE>",path_rule)
text_output = text_output.replace("<TESTFILE>",path_testfile)
text_output = text_output.replace("<LAMBDA>",text_lambda)

open("jane.config.final","w").write(text_output)