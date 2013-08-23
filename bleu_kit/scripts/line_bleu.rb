require "#{File.dirname(__FILE__)}/bleulib"

if ARGV.length < 2
  puts "Usage: ruby line_bleu.rb [options] [translation result] [references...]\n"
	puts "Option:"
	puts "-ngram min:max"
	puts "\tCalc from min-gram to max-gram(default 4:4)"
  exit
end

min = 4
max = 4
if ARGV[0] == "-ngram"
	ARGV.shift
	param = ARGV.shift
	if param =~ /(.+?):(.+?)/
		min = $1.to_i
		max = $2.to_i
	else
		throw "parse error"
	end
end

target = ARGV.shift
references = ARGV

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

tgt = openfile(target)
refss = references.map{|ref| openfile(ref)}

bleu = BLEU.new(tgt,refss, max)

tgt.each_index{|i|
	bleus = []
	max.downto(min){|n|
		bleus << bleu[i].calc_BLEU(n)
	}
	print bleus.join("\t"), "\t", tgt[i], "\n"
}

