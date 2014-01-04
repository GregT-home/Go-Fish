require_relative "../fishserver.rb"
#require_relative "../fishclient.rb"
#require_relative "../player.rb"
#require_relative "../result.rb"
#require_relative "../deck.rb"
#require_relative "../card.rb"
#require_relative "../hand.rb"
#require_relative "../game.rb"

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

    client1.close
    client2.close
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

    client1.close
    server.close
  end
end # .create_player

describe FishServer, ".put_message." do
  it "can send a message to a specific client" do
    server = FishServer.new(1)
#    server.debug

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    name = "Player One's Name"
    mclient = MockClient.new

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

    msg.should eq welcome_message

    mclient.close
    server.close
  end
end # .broadcast

describe FishServer, ".end_game" do
  context "Test .setup logic by creating 3 test hands." do
    before (:each) do
      @server = FishServer.new(3)

      # kick-off a non-blocking server thread
      thread_id = Thread.new { @server.get_clients }

      names = %w(One Two Three)
      @clients = [MockClient.new, MockClient.new, MockClient.new]

      #sending first for test purposes (avoids blocking)
      @clients.each_with_index { |c, i| c.send_line(names[i]) }

      @server.create_players

      @server.players[0].hand.should eq @server.game.current_hand
      @server.players[0].name.should eq names[0]
      @server.players[0].fd.should_not eq 0

      @clients[0].receive_message # consume "What is your name?" prompt
    end # before each

    after (:each) do
      @clients.each { |c| c.close }
      @server.close
    end

  it "can handle a single winner" do
      # cook the books :-)

      game = @server.game
      game.books[0]= ["2"]
      game.books[1]= ["4", "5", "A"]  # winner
      game.books[2]= ["8", "9"]

      @server.endgame
      msg = @clients[0].receive_message
      msg.should eql "========================="

      msg = @clients[0].receive_message
      msg.should eql "There are no more fish in the pond.  Game play is over.\n"
      msg = @clients[0].receive_message
      msg.should eql "Here is the final outcome:\n"

      msg = @clients[0].receive_message
      msg.should eql "Player 0, One, made 1 books (2s)"

      msg = @clients[0].receive_message
      msg.should eql "Player 1, Two, made 3 books (4s, 5s, As) and is the winner!\n"

      msg = @clients[0].receive_message
      msg.should eql "Player 2, Three, made 2 books (8s, 9s)"
  end

  it "can handle a tie" do
      # cook the books :-)

      game = @server.game
      game.books[0]= ["2"]
      game.books[1]= ["4", "5", "A"]  # winner 1
      game.books[2]= ["8", "9", "K"]  # winner 2

      @server.endgame
      msg = @clients[0].receive_message
      msg.should eql "========================="

      msg = @clients[0].receive_message
      msg.should eql "There are no more fish in the pond.  Game play is over.\n"
      msg = @clients[0].receive_message
      msg.should eql "Here is the final outcome:\n"

      msg = @clients[0].receive_message
      msg.should eql "Player 0, One, made 1 books (2s)"

      msg = @clients[0].receive_message
      msg.should eql "Player 1, Two, made 3 books (4s, 5s, As) and ties for the win!\n"
      msg = @clients[0].receive_message
      msg.should eql "Player 2, Three, made 3 books (8s, 9s, Ks) and ties for the win!\n"
    end
  end # context

end # .end_game
