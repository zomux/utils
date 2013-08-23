#!/bin/sh

#suffix
num=".num" #(num-num) to (num - num)
cut=".cut"

sed -e 's/\([0-9]\)\-\([0-9]\)/\1 \- \2/g' $1 > $1$num
sed -e 's/\([A-Za-z]\)\-\([A-Za-z]\)/\1 \2/g' $1$num > $1$cut

