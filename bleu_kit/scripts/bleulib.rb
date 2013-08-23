module JnMtLib
	# Create an array count of n.
	# Each elements are selected randomly from an interval of [0,max].
	def randext(n,max)
	  counter = 0

	  ret = []

	  while counter < n
	    id = rand(max)
	    ret << id
	    counter += 1
	  end
	  ret
	end

	def calc_line_ngram_count(words, n)
    c = words.length-n+1
    (c < 0)? words.length : c
	end

	def get_line_ngrams(words, n, ngram_count)
		ngrams = {}
		words.each_index{|idx|
			break if idx == ngram_count
			subwords = words[idx,n]
			ngrams[subwords] ||= 0
			ngrams[subwords] += 1
		}
		ngrams
	end

	#Calculate 'clip count' of each line..
	def calc_line_clip_count(tngrams, rngramss)
		clipcount = 0
		tngrams.each{|tngram, tnc|
			rnc = 0
			rngramss.each{|rngrams|
				next if rngrams[tngram] == nil
				rnc = rngrams[tngram] if rnc < rngrams[tngram]
			}
			clipcount += (rnc > tnc)? tnc : rnc
		}
		clipcount
	end

	def count_multi_ngrams(tws, rwss, n)
		tcount = 0
		clipcount = 0

		tws.each_index{|lidx|
			tline = tws[lidx]
			tnum= calc_line_ngram_count(tline, n)
			tcount += tnum
			
			tngrams = get_line_ngrams(tline, n, tnum)

			rngramss = []
			rwss.each{|rws|
				rnum = calc_line_ngram_count(rws[lidx], n)
				rngrams = get_line_ngrams(rws[lidx], n, rnum)

				rngramss << rngrams
			}

			clipcount += calc_line_clip_count(tngrams, rngramss)
		}
		[clipcount, tcount]
	end

	#calculate 'best match length'.
	def get_best_match_length(tlen, references)
		ret = nil
		mindist = nil
		references.map{|ref| ref.length}.each{|num|
			dist = (tlen-num).abs
			if mindist == nil or dist < mindist
				mindist = dist
				ret = num
			#elsif dist == mindist and num < ret
			#	ret = num
			end
		}
		ret
	end

	module_function :count_multi_ngrams, :randext, :get_best_match_length, :calc_line_ngram_count, :get_line_ngrams, :calc_line_clip_count
end

#Class for BLEU
class BLEU
	def wrap_array(arr, key)
		return nil if arr == nil
		val = arr[key]
		if val.instance_of?(Array)
			val	
		else
			[val]
		end
	end

	def gen_child_data(key)
		ncs = @ngram_clips.map{|nc| wrap_array(nc, key)	}
		tcs = @tcount.map{|tc| wrap_array(tc, key) }
		bml = wrap_array(@best_match_lengths, key)

		[ncs, tcs, bml, @ngram,@verbose]
	end

	# constructor
	# - target : an array of translation results
	# - references : an array of arrays of references
	# - n : n of ngram
	# - verbose : verbose mode
	def initialize(target, references, n=4, verbose=0)
		if target == nil
			@ngram_clips = references[0] #ncs
			@tcount = references[1] #tcs
			@best_match_lengths = references[2]
			@ngram = references[3]
			@verbose = references[4]
			return
		end

		if target.size != references[0].size and not references.inject(true){|pre, ref| pre and target.size == ref.size}
			throw "Array Size Mismatch!"
		end

		twords = target.map{|tgt| tgt.split }
		rwordss = references.map{|ref| ref.map{|rline| rline.split }}

		@verbose=verbose
		@ngram_clips = []
		@tcount = []
		@best_match_lengths = []
		@ngram = n

		(1..n).each{|m|
			@ngram_clips[m] = []
			@tcount[m] = []
			twords.each_index{|lidx|		
				tline = twords[lidx]
				tnum = JnMtLib.calc_line_ngram_count(tline, m)
				tngrams = JnMtLib.get_line_ngrams(tline, m, tnum)

				rngramss = []
				rwordss.each{|rwords|
					rline = rwords[lidx]
					rnum = JnMtLib.calc_line_ngram_count(rline, m)
					rngramss << JnMtLib.get_line_ngrams(rline, m, rnum)
				}

				@ngram_clips[m][lidx] = JnMtLib.calc_line_clip_count(tngrams, rngramss)
				@tcount[m][lidx] = tnum
			}
		}
		twords.each_index{|lidx|
			@best_match_lengths[lidx] = JnMtLib.get_best_match_length(twords[lidx].length, rwordss.map{|rws| rws[lidx]})
		}

	end

	# Create an instance of BLEU class which has only one element of the index of given key.
	def [](key)
		cdat = gen_child_data(key)
		BLEU.new(nil, cdat)
	end

	# Simply joint two instances of BLEU class.
	def +(bleu)
		throw "ngram size mismatch!" if @ngram != bleu.ngram

		newnc = []
		newtc = []
		(1..@ngram).each{|n|
			newnc[n] = @ngram_clips[n] + bleu.ngram_clips[n]
			newtc[n] = @tcount[n] + bleu.tcount[n]
		}
		
		v = nil
		if @verbose > bleu.verbose
			v=@verbose
		else
			v=bleu.verbose
		end

		BLEU.new(nil, [newnc, newtc, @best_match_lengths + bleu.best_match_lengths, @ngram,v])
	end

	# Calculate BLEU score.
	# - n : n of ngram
	#  - n is smaller than 'n' given for constructor.
	def calc_BLEU(n=@ngram)
		if n > @ngram
			throw "Error! #{n}gram > #{@ngram}gram"
		elsif n <= 0
			throw "Error! #{n}gram cannot be calculated."
		end

		nclip = @ngram_clips.map{|nc| 
			if nc == nil
				nil
			else
				nc.inject(0){|pre, c| pre+c}
			end
		}
		tc = @tcount.map{|t|
			if t == nil
				nil
			else
				t.inject(0){|pre, c| pre+c}
			end
		}

		pscore = []
		(1..n).each{|m|
			if tc[m] == 0
				throw "BUG!: clip count != 0 when count == 0" if nclip[m] != 0
				pscore << 0.0
			else
				pscore << nclip[m].to_f / tc[m]
			end

			if @verbose > 0
				puts "<ConcordanceRate ngram=#{m}>#{pscore[-1]}</ConcordanceRate>"
			end
		}
		c = tc[1]
		r = @best_match_lengths.inject(0){|pre, count| pre+count}
    bp = (c > r)? 1.0 : Math.exp(1.0-(r.to_f/c))
		if @verbose > 1
			puts "<CandidateLength>#{c}</CandidateLength>"
			puts "<BestMatchLength>#{r}</BestMatchLength>"
		end
		if @verbose > 0
			puts "<BrevityPenalty>#{bp}</BrevityPenalty>"
		end

    prebleu = 0.0
		(0...n).each{|psindex|
			return 0.0 if pscore[psindex] == 0.0
      prebleu += Math.log(pscore[psindex])/n.to_f
    }
    bleu = bp * Math.exp(prebleu)
	end
	attr_reader :ngram_clips, :tcount, :best_match_lengths, :ngram, :verbose
end

