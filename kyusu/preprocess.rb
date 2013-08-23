require 'moji'

STDOUT.sync = true

hyphentxt = "#{File.expand_path(File.dirname(__FILE__))}/hyphen.txt"
hyphen=nil
open(hyphentxt){|fp| hyphen = fp.gets.chomp}

while gets
	puts Moji.han_to_zen($_.chomp.gsub(hyphen,"-"))
end
