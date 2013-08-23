#binom.rb
require "#{File.dirname(__FILE__)}/bleulib"

if ARGV.size < 6
	$stderr.puts "ruby binom.rb [Random Seed] [Significance Level(%)] [divide num] [System1] [System2] [Reference..]"
	exit(1)
end

seed = ARGV.shift.to_i
sig_lev = ARGV.shift.to_f / 100
div_num = ARGV.shift.to_i
system1 = ARGV.shift
system2 = ARGV.shift
reffile = ARGV

srand(seed)

def read_data(fname)
	ret = []
	open(fname){|f|
		while f.gets
			$_.chomp!
			ret << $_
		end
	}
	ret
end

def init_divide(datsize,dn)
	num = datsize / dn
	reminder = datsize - num * dn
	num += 1 if reminder > 0

	tmp_dat = Array.new(datsize){|i| i}

	ret = Array.new(dn) { [] }
	dn.times{|i|
		num.times{
			idx = rand(tmp_dat.size)
			ret[i] << tmp_dat[idx]
			tmp_dat.delete_at(idx)
		}
		reminder -= 1
		num -= 1 if reminder == 0
	}

	ret
end

def divide(dat,initdat)
	ret = []
	initdat.each_index{|i|
		ret[i] = dat[initdat[i][0]]
		initdat[i][1..-1].each{|j|
			ret[i] += dat[j]
		}
	}
	ret
end

def factorial(n)
	ans = 1.0
	(1..n).each{|i|
		ans *= i
	}
	ans
end

def choose(n,k)
	factorial(n) / (factorial(k)*factorial(n-k))
end

def dbinom(n, k, p)
	choose(n,k) * (p**k) * ((1-p)**(n-k))
end

ref_dat = reffile.map{|fname| read_data(fname)}
sys1dat = read_data(system1)
sys2dat = read_data(system2)

sys1_total_bleu = BLEU.new(sys1dat, ref_dat)
printf("System1 total BLEU : %7.5s\n",sys1_total_bleu.calc_BLEU*100)

sys2_total_bleu = BLEU.new(sys2dat, ref_dat)
printf("System2 total BLEU : %7.5s\n",sys2_total_bleu.calc_BLEU*100)

initdat = init_divide(sys1dat.size, div_num)

sys1div = divide(sys1_total_bleu,initdat)
sys2div = divide(sys2_total_bleu,initdat)

sys1win = 0
sys2win = 0
draw = 0


puts "[times]\t[System1 BLEU]\t[System2 BLEU]\t[System1 win]\t[System2 win]\t[draw]"
div_num.times{|i|
	sys1bleu = sys1div[i].calc_BLEU
	sys2bleu = sys2div[i].calc_BLEU

	if sys1bleu > sys2bleu
		sys1win += 1
	elsif sys1bleu < sys2bleu
		sys2win += 1
	else
		draw += 1
	end
	printf("%d\t%7.5s\t\t%7.5s\t\t%d\t\t%d\t\t%d\n",i+1,sys1bleu*100,sys2bleu*100,sys1win,sys2win,draw)
}

puts "* System1 win: #{sys1win} times"
puts "* System2 win: #{sys2win} times"

if draw > 0
	$stderr.puts "Warning: There are some BLEU scores with draw(#{draw} times). Ignored."
end

puts "Null Hypothesis: System1 = System2"
puts "Alternative Hypothesis: System1 > System2"

total = sys1win + sys2win

prob = 0.0
(0..sys1win).each{|i|
	prob += dbinom(total, i, 0.5)
}

print "Pr{0 <= # of System1 Win <= #{sys1win}} = #{prob}"
if prob > 1 - sig_lev
	puts " > #{1-sig_lev}"
	puts "Null Hypothesis rejected"
else
	puts " <= #{1-sig_lev}"
	puts "Rejection failed."
end

