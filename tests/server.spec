require_relative "../FishServer.rb"
#require_relative "../FishClient.rb"
require_relative "../player.rb"
require_relative "../deck.rb"
require_relative "../card.rb"
require_relative "../hand.rb"
require_relative "../game.rb"

require "socket"

class MockClient
  attr_reader :socket

  def initialize(hostname='localhost',port=FishServer::PORT)
    @socket = TCPSocket.open(hostname,port)
    send_line("Hello") # initiate contact with the server
    receive_line
  end

  def send_line(string)
    @socket.puts string
  end

  def receive_line
    @socket.gets.chomp
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
    message
  end

  def close
    @socket.close
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
    server = FishServer.new(2)

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    client1=MockClient.new
    client2=MockClient.new

    server.client_fd.length.should eq 2
    server.close
  end
end # .get_clients

describe FishServer, ".create_player." do
  it "gets name and creates player from it" do
    server = FishServer.new(1)

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    name = "Player One's Name"
    client1=MockClient.new

    #sending first for test purposes (avoids blocking)
    client1.send_line(name)

    server.create_players
    server.players[0].hand.should eq server.game.current_hand
    server.players[0].name.should eq name
    server.players[0].fd.should_not eq 0
    server.close
  end
end # .create_player

describe FishServer, ".put_message." do
  it "can send a message to a specific client" do
    server = FishServer.new(1)

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    name = "Player One's Name"
    mclient=MockClient.new

    #sending name first for test purposes (avoids blocking)
    mclient.send_line(name)

    server.create_players

    # we know that server.create_players issued a prompt to the
    # client: consume it.
    mclient.consume_message

    welcome_message = <<EOM
Welcome to the Fish Server

EOM
    server.put_message(server.players[0].fd, welcome_message)

    msg = mclient.receive_message

    msg.should eq welcome_message
  end
end # .put_message

describe FishServer, ".broadcast." do
  it "can send a message to all clients" do
    server = FishServer.new(1)

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    name = "Player One's Name"
    mclient=MockClient.new

    #sending name first for test purposes (avoids blocking)
    mclient.send_line(name)
    server.create_players
    mclient.consume_message

    welcome_message = <<EOM
Welcome to the Fish Server

EOM
    server.broadcast(welcome_message)

    msg = mclient.receive_message

    msg.should eq welcome_message
    server.close
  end
end # .broadcast


describe FishServer, ".check_all_for_books" do
  it "tbd.: checks each player's hand for books" do
    server = FishServer.new(1)

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    name = "Player One's Name"
    mclient=MockClient.new

    #sending name first for test purposes (avoids blocking)
    mclient.send_line(name)
    server.create_players
    mclient.consume_message

    welcome_message = <<EOM
Welcome to the Fish Server

EOM
    server.broadcast(welcome_message)

    msg = mclient.receive_message

    msg.should eq welcome_message

  end
end # .check_all_for_books

