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
    clients[-1]
  end

  def put_line(fd, line)
    fd.puts line
  end

  def put_message(fd, msg)
    fd.puts msg + EOM_TOKEN
  end

  def broadcast(msg)
    @clients.map { |cli|
      put_message(cli, msg)
    }
  end

  def get_line(fd)
    fd.gets.chomp
  end

  def close
    @server.close
    @clients.each { |fd| fd.close }
    @clients.clear
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
