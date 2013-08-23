require 'moji'

STDOUT.sync = true

deletetxt="#{File.dirname(__FILE__)}/delete.txt"
deletes = []
open(deletetxt){|fp|
	while fp.gets
		$_.chomp!
		deletes << $_
	end
}

while gets
	line=$_.chomp
	joinflg=false

	output = []
	words = line.split
	words.each_index{|i|
		word = words[i]
		if Moji.type?(word[-1], Moji::ZEN_ALNUM)
			if joinflg
				output[-1] += word
			else
				output << word
			end

			joinflg=true
		else
			output << word
			joinflg=false
		end
	}

	output.each{|word|
		deletes.each{|c|
			word.delete!(c)
		}
	}
	output.delete("")
	
	puts output.join(" ")
end
