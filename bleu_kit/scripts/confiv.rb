require "#{File.dirname(__FILE__)}/bleulib"

if ARGV.size < 5
	puts "ruby #{__FILE__} [options] [seed] [iter_num] [Significance Level(%)] [System result] [Reference..]"
	exit 1
end

gnuplot = false
if ARGV[0] == "--gnuplot"
	gnuplot = true
	ARGV.shift
end

seed = ARGV.shift.to_i
itr = ARGV.shift.to_i

siglevel = ARGV.shift.to_f/100.0
systemres = ARGV.shift
ref = ARGV

srand seed

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

result = openfile(systemres)
references = ref.map{|fname| openfile(fname)}

bleu = BLEU.new(result, references)

num = result.size

bleus = []

counter = 0
puts "[itr]\t[system BLEU]" if not gnuplot

(1..itr).each{|i|
	counter += 1

	if counter % 100 == 0 and gnuplot
		$stderr.puts "#{counter} times"
	end

	idxs = JnMtLib.randext(num,num)
	tmpbleu = bleu[idxs[0]]
	
	
	idxs[1..-1].each{|k|
		tmpbleu += bleu[k]
	}

	bleus << tmpbleu.calc_BLEU

	puts "#{counter}\t#{bleus[-1]}" if not gnuplot
}

bleus.sort!

puts "#{counter} times iterated." if not gnuplot
cutnum = ((itr * (1.0-siglevel))/2.0).to_i

puts "#{siglevel*100}% significance level is from No.#{cutnum+1} to No.#{counter-cutnum} when sorted by BLEU score." if not gnuplot

if not gnuplot
	puts "#{bleus[cutnum]} <= SYSTEM BLEU <= #{bleus[-cutnum-1]}"
else
	puts "#{bleu.calc_BLEU}\t#{bleus[cutnum]}\t#{bleus[-cutnum-1]}"
end

