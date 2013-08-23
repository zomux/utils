require "#{File.expand_path(File.dirname(__FILE__))}/config.rb"

conffile = "#{File.dirname(__FILE__)}/conf.txt"
if ARGV[0]=="--conf"
	ARGV.shift
	conffile=File.expand_path(ARGV.shift)
end

conf = BigLM::Config.new(conffile)

reader = ARGV.shift
fname = ARGV.shift

conf.logger.info "Tokenizer: #{conf.tokenizer}"
conf.logger.info "Tokenizer option: #{conf.tokenizeroption}"

version=`#{conf.tokenizer} #{conf.tokenizerversion}`
version=version.split("\n").join(", ")

conf.logger.info "Tokenizer version: #{version}"

conf.logger.info "Start tokenizing #{fname}"

command  = "#{reader} #{fname} "
command += "| ruby #{File.dirname(__FILE__)}/preprocess.rb "
command += "| #{conf.tokenizer} #{conf.tokenizeroption} "
command += "| ruby #{File.dirname(__FILE__)}/postprocess.rb "

conf.logger.info "Execute: #{command}"

system(command)

conf.logger.info "End tokenizing #{fname}"

