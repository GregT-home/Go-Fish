require_relative "./fishserver.rb"
require 'socket'

class FishClient
  attr_reader :socket

  # it can connect to the server
  def initialize(hostname = 'localhost', port = FishServer::PORT)
    @socket = TCPSocket.open(hostname, port)
    send_line("Hello").inspect # initiate contact with the server
    receive_line.inspect
  end

  # it can send a single line message to the server
  def send_line(string)
    begin
      @socket.puts string

    rescue => reason
      puts "Server error: #{reason.to_s}"
      puts "You have exited the game."
    end
  end

  # it can receive a single-line message from the server
  def receive_line
    @socket.gets.chomp
  end

  # it can receive a multi-line message from the server
  def receive_message
    message = ""
    begin
      message += receive_line + "\n"
      eom = Regexp.new(FishServer::EOM_TOKEN)
      if eom.match(message)
        message[FishServer::EOM_TOKEN+"\n"]=""
        break
      end
    end while true
    eog = Regexp.new(FishServer::GAME_OVER_TOKEN)
    exit if eog.match(message)
    message
  end

  def close
    @socket.close
    @thread_id.kill
  end

  def display_server_messages
    @thread_id = Thread.new {
      loop do
        puts receive_message
      end
    }
  end
end #FishClient
