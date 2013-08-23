#coding: utf8
"""
merge phrase by juman 

TODO:
1. get result from mecab  : readcorpus
2. parse by juman  : parse_by_juman
3. find setsubiji  : find_setsubiji
4. merge words : merge_words  -> list of phrase merged
5. replace the orignal words by merged phrase : replace_phrases
6. output : output_results

GPL Liscensed 


"""

import os,sys

def load_juman_results():
  global juman_results
  print "loading juman results..."
  juman_results = open('ja.juman').read().split("EOS\n")

def read_juman_result(i):
  global juman_results
  return juman_results[i]

def readcorpus(file_of_mecab):
  """
  return lines
  """
  return open( file_of_mecab).readlines()

def parse_by_juman(str):
  """
  return result of juman
  """

  return os.popen("echo \"%s\" | juman -b" % str.replace(" ","")).read()
  

def find_setsubiji_and_merge_words(result_of_juman):
  """
  return a list of merged words 
  [ phrase , ... ]
  """
  lines = result_of_juman.split("\n")
  list_words = []
  list_phrase = []
  current_found_phrase = None
  for line in lines:
    pair = line.split(" ")
    if len(pair) < 5: continue
    word = pair[0]
    cate = pair[5]
    if cate == "動詞性接尾辞" and not current_found_phrase:
      current_found_phrase = list_words[-1]
    if current_found_phrase and cate != "動詞性接尾辞" :
      list_phrase.append(current_found_phrase)
      current_found_phrase = None
    if current_found_phrase and cate == "動詞性接尾辞":
       current_found_phrase += " "+word

    
    list_words.append(word)

  return list_words,list_phrase



def replace_phrases(list_of_words,list_of_phrase):
  """
  return result replaced
  """
  str_words = " ".join(list_of_words)
  list_of_phrase.sort(key=lambda x: x.count(" ") , reverse=True)
  for phrase_with_space in list_of_phrase:
    str_words = str_words.replace(phrase_with_space,phrase_with_space.replace(" ",""))
  


  return str_words

def output_result(str,file_output):
  global file_handle_of_output
  #print str
  file_handle_of_output.write(str+"\n")




if __name__ == "__main__":
  usage = """
  python mergephrase.py file_of_mecab file_to_output
  """
  if len(sys.argv) < 3:
    print usage
    sys.exit()
  if len(sys.argv) == 3:
    #python mergephrase.py file_of_mecab file_to_output
    file_of_mecab = sys.argv[1]
    file_to_output = sys.argv[2]
    file_handle_of_output = open(file_to_output,"w")
    lines = readcorpus( file_of_mecab )
    load_juman_results()
    i = 0
    print "juman suffix merging ... "
    for line in lines:
      if i % 10000 == 0 : print i
      line_juman = read_juman_result(i)
      list_words,list_phrase = find_setsubiji_and_merge_words( line_juman )
      line = replace_phrases( list_words ,list_phrase )
      output_result(line , file_to_output )
      i += 1
  else:
    command = sys.argv[1]
    if command == "--merge-sahen":
      print "merge sa-hen verb with suffix ..."
      file_input = sys.argv[2]
      file_output = sys.argv[3]
      foutput = open(file_output,"w")
      lines = open(file_input).xreadlines()
      load_juman_results()
      n = 0
      for line in lines:
        if n % 10000 == 0 : print n
        line = line.strip()
        juman_result = read_juman_result(n)
        mapWordDetial = {}
        for line_j in juman_result.split("\n"):
          if line_j.count(" ") < 2: continue
          word,detail = line_j.split(" ",1)
          mapWordDetial[word] = detail
        words = line.split(" ")
        words_new = []
        matched = False
        for i,word in enumerate(words):
          if word in mapWordDetial and i < len(words)-1: 
            detail = mapWordDetial[word]
            if detail.count("サ変名詞")>0 or detail.count("動詞")>0:
              if words[i+1] in ['する','される','した','し','されている','された','して','され','させる','している','されて','されており','させ','させて']:
                words_new.append(word+words[i+1])
                matched = True
                continue
          if matched :
            matched = False
          else :
            words_new.append(word)
        line = " ".join(words_new)
        foutput.write(line+"\n")
        
        n += 1
      foutput.close()
