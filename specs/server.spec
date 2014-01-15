require_relative "../fishserver.rb"
require "socket"

#Hand_str_regexp = Regexp.new("\[|10|[2-9]|[JQKA]|-[CDHS]]", true)

class MockClient
  attr_reader :socket

  def initialize(hostname='localhost',port=FishServer::PORT)
    @debug = true
puts "mc: we got here"
    @socket = TCPSocket.open(hostname,port)
puts "mc: we got here 2"
    send_line("Hello") # initiate contact with the server
puts "mc: we got here 3"
    receive_line
puts "mc: returning from .new"
  end

  def send_line(string)
    @socket.puts string
  end

  def consume_message
    message = ""
    begin
      message += receive_line + "\n"
      if /:EOM:/.match(message)
        message[FishServer::EOM_TOKEN+"\n"]=""
        break
      end
    end while true
  end

  def receive_message
    message = ""
    begin
      message += receive_line + "\n"
      if /:EOM:/.match(message)
        message[FishServer::EOM_TOKEN+"\n"]=""
        break
      end
    end while true
    log "receive_message returning: #{message}"
    message
  end

  def close
    log "closing #{socket.inspect}"
    @socket.close
  end

  def debug
    @debug = ! @debug
  end

private
  def receive_line
    @socket.gets.chomp
  end

  def log(message)
    STDOUT.puts "Client Log: " + message if @debug
  end

end # MockClient

describe FishServer, ".new: can create a server" do
  it ".new: for one clients" do
    server = FishServer.new(1)
    server.number_of_players.should eq 1
    server.close
  end 

  it ".new: for two clients" do
    server = FishServer.new(2)
    server.number_of_players.should eq 2
    server.close
  end 
end # end .new

describe FishServer, ".get_clients." do
  it "accepts multiple clients" do
puts "", "Calling FishServer.new(2/multiple)"
    server = FishServer.new(2)

#     #sending first for test purposes (avoids blocking)
#     client1.send_line(name)

    # kick-off a non-blocking server thread
    thread_id = Thread.new do
      while @server.clients.count < 2 do
        server.accept_clients
        puts "client accepted"
      end
    end

puts "","we got here 1"
    client1=MockClient.new
puts "","we got here 2"
    client2=MockClient.new
puts "","we got here"

    server.client.count.should eq 2
puts "","we got here"

    client1.close
    client2.close
    server.close
  end
end # .get_clients

# describe FishServer, ".create_player." do
#   it "gets name and creates player from it" do
#     server = FishServer.new(1)

#     # kick-off a non-blocking server thread
#     thread_id = Thread.new { server.get_clients }

#     name = "Player One's Name"
#     client1=MockClient.new

#     #sending first for test purposes (avoids blocking)
#     client1.send_line(name)

#     server.create_players
#     server.players[0].hand.should eq server.game.current_hand
#     server.players[0].name.should eq name
#     server.players[0].socket.should_not eq 0

#     client1.close
#     server.close
#   end
# end # .create_player

describe FishServer, ".put_message." do
  it "can send a message to a specific client" do
    server = FishServer.new(1)

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    name = "Player One's Name"
    mclient = MockClient.new

    #sending name first for test purposes (avoids blocking)
    mclient.send_line(name)

    #accept the client
    @server.accept

    # we know that server.create_players issued a prompt to the
    # client: consume it.
    mclient.consume_message

    welcome_message = <<EOM
    Welcome to the Fish Server

EOM
    server.put_message(server.client[0], welcome_message)
    msg = mclient.receive_message
    msg.should =~ Game::Hand_str_regexp
#<><>    
    msg = mclient.receive_message.strip
    msg.should eq welcome_message.strip

    mclient.close
    server.close
  end
end # .put_message

describe FishServer, ".broadcast." do
  it "can send a message to all clients" do
    server = FishServer.new(1)

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    name = "Player One's Name"
    mclient = MockClient.new

    #sending name first for test purposes (avoids blocking)
    mclient.send_line(name)
    server.create_players
    mclient.consume_message

    welcome_message = <<EOM
    Welcome to the Fish Server

EOM
    server.broadcast(welcome_message)

    msg = mclient.receive_message
    msg.should =~ Game::Hand_str_regexp

    msg = mclient.receive_message.strip
    msg.should eq welcome_message.strip

    mclient.close
    server.close
  end
end # .broadcast
