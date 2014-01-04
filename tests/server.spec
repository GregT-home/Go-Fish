require_relative "../fishserver.rb"
require "socket"

Hand_str_regexp = Regexp.new("\[|10|[2-9]|[JQKA]|-[CDHS]]", true)

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

    server.client.length.should eq 2

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
    server.players[0].hand.should eq server.game.hands[server.game.current]
    server.players[0].name.should eq name
    server.players[0].socket.should_not eq 0

    client1.close
    server.close
  end
end # .create_player

describe FishServer, ".put_message." do
  it "can send a message to a specific client" do
    server = FishServer.new(1)

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
    server.put_message(server.players[0].socket, welcome_message)

    msg = mclient.receive_message
    msg.should =~ Hand_str_regexp
    
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
    msg.should =~ Hand_str_regexp

    msg = mclient.receive_message.strip
    msg.should eq welcome_message.strip

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

      @server.players[0].hand.should eq @server.game.hands[@server.game.current]
      @server.players[0].name.should eq names[0]
      @server.players[0].socket.should_not eq 0

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
      msg.should =~ Hand_str_regexp

      target_msg =<<-EOF
=========================
There are no more fish in the pond.  Game play is over.
Here is the final outcome:
EOF
      msg = @clients[0].receive_message.strip
      msg.should eql target_msg.strip

      msg = @clients[0].receive_message.strip
      msg.should eql "Player 0, One, made 1 books (2s)"

      msg = @clients[0].receive_message.strip
      msg.should eql "Player 1, Two, made 3 books (4s, 5s, As) and is the winner!"

      msg = @clients[0].receive_message.strip
      msg.should eql "Player 2, Three, made 2 books (8s, 9s)"
  end

  it "can handle a tie" do
      # cook the books :-)

      game = @server.game
      game.books[0]= ["2"]
      game.books[1]= ["4", "5", "A"]  # winner 1
      game.books[2]= ["8", "9", "K"]  # winner 2

      @server.endgame

      msg = @clients[0].receive_message.strip
      msg.should =~ Hand_str_regexp

      target_msg =<<-EOF
=========================
There are no more fish in the pond.  Game play is over.
Here is the final outcome:
EOF
      msg = @clients[0].receive_message.strip
      msg.should eql target_msg.strip

      msg = @clients[0].receive_message.strip
      msg.should eql "Player 0, One, made 1 books (2s)"

      msg = @clients[0].receive_message.strip
      msg.should eql "Player 1, Two, made 3 books (4s, 5s, As) and ties for the win!"
      msg = @clients[0].receive_message.strip
      msg.should eql "Player 2, Three, made 3 books (8s, 9s, Ks) and ties for the win!"
    end
  end # context
end # .end_game

describe FishServer, "." do
  context "Create 3 test hands." do
    before (:each) do
      @server = FishServer.new(3)

      # kick-off a non-blocking server thread
      thread_id = Thread.new { @server.get_clients }

      names = %w(One Two Three)
      @clients = [MockClient.new, MockClient.new, MockClient.new]

      #sending first for test purposes (avoids blocking)
      @clients.each_with_index { |c, i| c.send_line(names[i]) }

      @server.create_players

#puts ""; @server.players.each_with_index { |player, i| puts "Player[#{i}] hand: #{player.hand.to_s}" }


      @server.players[0].hand.should eq @server.game.hands[@server.game.current]
      @server.players[0].name.should eq names[0]
      @server.players[0].socket.should_not eq 0

      # consume "What is your name?" prompt
      @clients.map {|client| client.receive_message }
      # consume card display
      @clients.map {|client| client.receive_message }

    end # before each

    after (:each) do
      @clients.each { |c| c.close }
      @server.close
    end

    it ".put_status: can display multiple player status" do
      @server.game.books[1] << "Q"
      @server.game.books[1] << "2"
      @server.game.books[1] << "7"
      @server.game.books[2] << "A"

      @server.put_status(@server.players[0].socket)
      test_msg = "One (#0) has 7 cards and has made 0 books ()"
      msg = @clients[0].receive_message.strip
      msg.should eq test_msg  

      @server.put_status(@server.players[0].socket)
      test_msg = "Two (#1) has 7 cards and has made 3 books (2s, 7s, Qs)"
      msg = @clients[0].receive_message.strip
      msg.should eq test_msg  

      @server.put_status(@server.players[0].socket)
      test_msg = "Three (#2) has 7 cards and has made 1 books (As)"
      msg = @clients[0].receive_message.strip
      msg.should eq test_msg  
    end

    it ".calculate_rankings: it determines player ranking" do

      @server.game.books[1] << "Q" # Player 1 wins with 3
      @server.game.books[1] << "2"
      @server.game.books[1] << "7"
      @server.game.books[2] << "A" # Player 2 comes second, 0 is third

      rank_list = @server.calculate_rankings
      rank_list.should eq [2, 0, 1]

    end

    it ".calculate_rankings: it shows ties" do

      @server.game.books[1] << "Q" # Player 1 and 2 both have 2
      @server.game.books[1] << "2" # and tie for win
      @server.game.books[2] << "7"
      @server.game.books[2] << "A" 

      rank_list = @server.calculate_rankings
      rank_list.should eq [1, 0, 0]

    end

    it ".parse_ask can split raw input into player and rank" do
      player_num, rank = @server.parse_ask("ask 1 for 3s")
      player_num.should eq 1
      rank.should eq "3"

      player_num, rank = @server.parse_ask("ask 1 3")
      player_num.should eq 1
      rank.should eq "3"

      player_num, rank = @server.parse_ask("ask Player 1, have any 3s?")
      player_num.should eq 1
      rank.should eq "3"
    end

    it ".process_commands: prints help when it does not understand" do
      type = @server.process_commands(@server.players[0], "hello")
      
      type.should eq :private

      test_regexp = Regexp.new("Not understood.*")
      msg = @clients[0].receive_message.strip
      msg.should =~ test_regexp
     end
 
   it ".process_commands: understands deck size and shows it" do
      type = @server.process_commands(@server.players[0], "deck size")
      
      type.should eq :private
      test_regexp = Regexp.new("\\d+ card.* are left in the pond")
      msg = @clients[0].receive_message.strip
      msg.should =~ test_regexp
     end

   it ".process_commands: understands hand and prints cards" do
      type = @server.process_commands(@server.players[0], "hand")
      
      type.should eq :private

      test_regexp = Hand_str_regexp

      msg = @clients[0].receive_message.strip
      msg.should =~ test_regexp
     end

   it ".process_commands: understands status and shows it" do
      type = @server.process_commands(@server.players[0], "status")
      
      type.should eq :private

      test_regexp = Regexp.new(".*has \\d+ cards and has made \\d+ book.*")
      msg = @clients[0].receive_message.strip
      msg.should =~ test_regexp
     end

   it ".process_commands: understands well-formed ask and processes it" do
      type = @server.process_commands(@server.players[0], "ask 1 for 3s")
      
      type.should eq :public

      test_regexp = Regexp.new(".*(player .*)asked for .* from player #.*")
      msg = @clients[0].receive_message.strip
      msg.should =~ test_regexp
     end

   it ".process_commands: understands well-formed ask with invalid player and processes it" do
      type = @server.process_commands(@server.players[0], "ask 10 for 3s")
      
      type.should eq :private

      test_regexp = Regexp.new("That player does not exist.")
      msg = @clients[0].receive_message.strip
      msg.should =~ test_regexp
     end

   it ".process_commands: handles badly-formed ask properly" do
      type = @server.process_commands(@server.players[0], "ask feep for 3s")
      
      type.should eq :private

      test_msg = "Victim number not recognized."
      msg = @clients[0].receive_message.strip
      msg.should eq test_msg
     end

   it ".process_commands: does not allow non-existent players to be asked" do
      type = @server.process_commands(@server.players[0], "ask 5 for 3s")
      
      type.should eq :private

      test_msg = "That player does not exist."
      msg = @clients[0].receive_message.strip
      msg.should eq test_msg
     end
  end
end
