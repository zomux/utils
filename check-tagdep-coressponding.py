import os,sys

fen = open("data.en")
ftagdep = open("data.en.tagdep")

line = fen.readline()
lines_tag = ftagdep.read().split("\n\n")
nline = 0

while line:
    line = line.strip()
    line_tag = lines_tag[nline*2]
    line_tag = line_tag.strip()
    line_tagx = " ".join([wp.split("/")[0] for wp in line_tag.split(" ")])
    firstword = line[0]
    if firstword not in ["\"","(","-","*"] and firstword != line_tagx[0]:
        print nline
        print line
        print line_tag

    line = fen.readline()
    line_tag = ftagdep.readline()
    line_tag = ftagdep.readline()
    nline += 1