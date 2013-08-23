require 'logger'

module BigLM
	class Config
		def initialize(conffile)
			@conf = {}
			open(conffile){|fp|
				while fp.gets
					name, value = $_.chomp.split(":")
					name.downcase!
					@conf[name] ||= []
					@conf[name] << value
				end
			}

			@conf.each{|name, values|
				Config.define_getter(name, values)
			}

			@logger = Logger.new File.expand_path(logfile)
			@logger.level = eval("Logger::#{loglevel}")
		end

		def self.define_getter(name,values)
			define_method("#{name}_array"){
				values
			}
			define_method(name){
				values[0]
			}
		end
		attr_reader :logger
	end

end

