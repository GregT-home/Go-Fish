require_relative "../FishServer.rb"
#require_relative "../FishClient.rb"
require_relative "../player.rb"
require_relative "../result.rb"
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
    server.close
  end
end # .broadcast


describe FishServer, ".check_all_for_books" do
  it "check each player's hand for books and broadcast results" do

    # stack a deck so that 2nd hand has a book
    test_hand_size = 7
    number_of_test_hands = 2
    target_hand, stacked_deck = [],[]
    target_hand[0] = "2C 2H 3C QH 5C 4H 9H".split
    target_hand[1] = "10C 10H 10S 10D 2S 2D 9S".split
    test_hand_size.downto(0) { |card_num| 
      number_of_test_hands.times { |hand_num|
        stacked_deck << target_hand[hand_num][card_num]
      }
    }
    stacked_cards_string = stacked_deck.join(" ")

    server = FishServer.new(2, Card.new_cards_from_s(stacked_cards_string))

    # kick-off a non-blocking server thread
    thread_id = Thread.new { server.get_clients }

    name1 = "******* Player One's Name"
    mclient1 = MockClient.new

    name2 = "******* Player Two's Name"
    mclient2 = MockClient.new

    #sending names first for test purposes (avoids blocking)
    mclient1.send_line(name1)
    mclient2.send_line(name2)

    server.create_players

    mclient1.consume_message
    mclient2.consume_message

    server.game.hands.length.should be 2
    server.game.hands.length.times { |i|
      server.game.hands[i].length.should be 7
    }

    server.game.current_hand.should == server.game.hands[0]
    
    i = 0
    server.game.check_all_for_books { |result|
      result.number_of_books_made.should == 0 if i == 0
      result.number_of_books_made.should == 1 if i == 1
      puts result.to_s
      i = i + 1
      }

    expect {server.game.check_all_for_books}.to raise_error
  end
end # .check_all_for_books

