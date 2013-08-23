require "#{File.dirname(__FILE__)}/bleulib"

if ARGV.size < 5
	puts "ruby #{__FILE__} [seed] [iter] [System1 Result] [System2 Result] [Reference..]"
	exit 1
end

seed = ARGV.shift.to_i
itr = ARGV.shift.to_i

target1 = ARGV.shift
target2 = ARGV.shift

references = ARGV

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

tgt1 = openfile(target1)
tgt2 = openfile(target2)
refss = references.map{|fname| openfile(fname)}

num = tgt1.size

counter_tgt1 = 0
counter_tgt2 = 0
counter_equal = 0
print "[system1 BLEU]\t[system2 BLEU]\t[system1 win]\t[system2 win]\t[draw]\n"

tgt1bleu = BLEU.new(tgt1, refss)
tgt2bleu = BLEU.new(tgt2, refss)

(1..itr).each{|i|
	idxs = JnMtLib.randext(num,num)
	
	tmptgt1 = tgt1bleu[idxs[0]]
	idxs[1..-1].each{|k|
	 tmptgt1 = tmptgt1 + tgt1bleu[k]
	}

	tmptgt2 = tgt2bleu[idxs[0]]
	idxs[1..-1].each{|k|
	 tmptgt2 = tmptgt2 + tgt2bleu[k]
	}

	r = [tmptgt1.calc_BLEU,tmptgt2.calc_BLEU]
	print r.join("\t"),"\t"
	if r[0] < r[1]
		counter_tgt2 += 1
	elsif r[0] > r[1]
		counter_tgt1 += 1
	else
		counter_equal += 1
	end
	print [counter_tgt1,counter_tgt2,counter_equal].join("\t"),"\n"
}

print "system1:",counter_tgt1,"\n"
print "system2:",counter_tgt2,"\n"
print "draw:", counter_equal,"\n"

