#!/bin/sh

echo "*** BLEU score for document ***"
command_doc='ruby ../scripts/doc_bleu.rb tgt1 ref'
echo $command_doc
$command_doc

echo ""
echo "*** BLEU score for each lines ***"
command_line='ruby ../scripts/line_bleu.rb -ngram 1:4 tgt1 ref'
echo $command_line
$command_line

echo ""
echo "*** Bootstrap testing ***"
command_bootstrap='ruby ../scripts/bootstrap.rb 131 10 tgt1 tgt2 ref'
echo $command_bootstrap
$command_bootstrap

echo ""
echo "*** Binomial testing ***"
command_binom='ruby ../scripts/binom.rb 131 5 5 tgt1 tgt2 ref'
echo $command_binom
$command_binom

echo ""
echo "*** Confidence Interval ***"
command_confiv='ruby ../scripts/confiv.rb 131 100 95 tgt1 ref'
echo $command_confiv
$command_confiv

