require_relative "./FishServer.rb"

print "How many players for this game? "
num = gets.chomp.strip.to_i

server = FishServer(num)

server.run

server.close
