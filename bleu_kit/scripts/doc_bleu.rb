require 'optparse'
require "#{File.dirname(__FILE__)}/bleulib"

opt = OptionParser.new

if ARGV.size < 2
	puts "Usage: ruby #{__FILE__} [option] [Translation Result] [Reference...]"
	puts "option: -v level, --ngram n"
	exit(1)
end

verbose = 0
ngram = 4

opt.on('-v VAL'){|v|
	verbose = v.to_i
}

opt.on('--ngram VAL'){|v|
	ngram = v.to_i
}

opt.parse!(ARGV)

target = ARGV.shift
ref = ARGV

def openfile(fname)
  ret = []
  open(fname){|f|
    while f.gets
        $_.chomp!
        ret << $_
    end
  }
  ret
end

ts = openfile(target)
rs = ref.map{|fname| openfile(fname)}

puts "<DocBLEU>" if verbose > 0
bleu = BLEU.new(ts, rs, ngram,verbose)
if verbose > 1
	(1..ngram).each{|n|
		puts "<NgramBLEU ngram=#{n}>"
		nbleu = bleu.calc_BLEU(n) * 100
		puts "<BLEU ngram=#{n}>#{nbleu}</BLEU>"
		puts "</NgramBLEU>"
	}
else
	bleuscore = bleu.calc_BLEU * 100
	print "<BLEU ngram=#{ngram}>" if verbose > 0
	print bleuscore
	puts "</BLEU>" if verbose > 0
end
puts "</DocBLEU>" if verbose > 0

