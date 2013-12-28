require 'socket'

class FishServer
  PORT = 54011
  EOM_TOKEN = ":EOM:"

attr_reader :clients

  def initialize()
    @clients = []
    @server = TCPServer.open(PORT)	# listen on our port
  end

  def accept_client
    clients << @server.accept
  end

  def preceive(client)
    client.gets.chomp
  end

  def psend(client, msg)
    client.puts msg
  end

  def broadcast
    @clients.each { |cli|
      cli.puts(cli.gets.schomp)
    }
  end

  def close
    @server.close
    @clients.each { |fd| fd.close }

  end

end # Fish_Server
# class Player
#   attr_reader :fd, :name, :hand, :next_hand_number

#   def initialize(name="", fd, hand)
#     @next_hand_to_assign = @next_hand_number ? @next_hand_number + 1 : 0
#     @name = "Unknown Player #{next_hand_number}" if name == ""
#     @fd = fd
#     @hand = hand
#   end
# end # Player
