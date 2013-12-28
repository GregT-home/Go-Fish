require 'socket'

class FishClient
  # it can connect to the server
  def initialize(hostname='localhost',port=FishServer::PORT)
    @socket = TCPSocket.open(hostname,port)
  end

  # it can send a single line message to the server
  def send_line(string)
    @socket.puts string
  end

  # it can receive a single-line message from the server
  def receive_line
    @socket.gets.chomp
  end

  # it can receive a multi-line message from the server
  def receive_message
    message = ""

    until (line = receive_line) == FishServer::EOM_TOKEN
      message += line + "\n"
    end
    message
  end

end #FishClient
