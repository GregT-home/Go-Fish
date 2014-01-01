require_relative "./FishServer.rb"

# take # of players from command line, if present
num = ARGV.length > 0 ? ARGV[0].to_i : 0

# get it from terminal, if not in command line
until num >= 2 && num <= 10
  print "How many players for this game (2-10)? "
  num = gets.chomp.strip.to_i
end

puts "Creating a Fish Server for #{num} players..."
server = FishServer.new(num)

server.run

server.close
