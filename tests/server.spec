require_relative "../FishServer.rb"
require_relative "../FishClient.rb"
require_relative "../player.rb"
#require_relative "../hand.rb"
#require_relative "../game.rb"

require "socket"

describe FishServer, "receives from, and sends to clients" do
  context ".new: Create a test server and two client connections" do
    # create a standard server
    before (:each) do
      @server = FishServer.new

      @client1 = FishClient.new("localhost")
      @client2 = FishClient.new("localhost")
      
      # clients send to server first, for test purposes.
      # first answer is the name of the player
      test_msg1 = "client 1: Player One"
      test_msg2 = "client 2: Player Two"
      @client2.send_line test_msg2
      @client1.send_line test_msg1

      @c1fd = @server.accept_client
      @c2fd = @server.accept_client
      @server.clients.length.should == 2

      msg = @server.get_line(@c1fd)
      msg.should == test_msg1
      msg = @server.get_line(@c2fd)
      msg.should == test_msg2
    end

    # close when done
    after (:each) do
      @server.close
      @client1.close
      @client2.close
    end

    it ".put_message: can send a multi-line message to a client" do

      welcome_message = <<EOM
Welcome to the Fish Server

EOM
      @server.put_message(@c1fd, welcome_message)

      msg =  @client1.receive_message
      msg.should == welcome_message
    end

    it ".get_line: can request and receive a player name" do
      prompt = "What is your name: "
      @server.put_message(@c1fd, prompt)
      response =  @client1.receive_message
      response.should == prompt

      name_msg = "Player One"
      @client1.send_line(name_msg)

      msg =  @server.get_line(@c1fd)
      msg.should == name_msg
    end      

    it ".broadcast: can send a message to all connected clients" do
      bcast_msg="This is a broadcast message\nTesting 1, 2, 3\n"
      @server.broadcast(bcast_msg)

      [@client1, @client2].map { |cli|
        client_sees = cli.receive_message
        client_sees.should == bcast_msg
      }
    end      

    it "can start a game and run a null round" do
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
      # extra_cards = "3H".split
      # extra_cards.map { |card_string| stacked_deck << card_string }

      stacked_cards_string = stacked_deck.join(" ")
      game = Game.new(number_of_test_hands,
                       Card.new_cards_from_s(stacked_cards_string))

      game.hands.length.should be number_of_test_hands
      game.hands.length.times { |i|
        game.hands[i].length.should be test_hand_size
      }

      player1 = Player.new(game.current_hand, "Name: Player One", @c1fd)
      game.advance_to_next_hand
      player2 = Player.new(game.current_hand, "Name: Player Two", @c2fd)
      game.advance_to_next_hand

      game.current_hand.should == game.hands[0]
      
      result = {}
      [player1, player2].map { |player|
        player.hand.cards.map { |card|
          result[player] = game.ask_for_matches(player.hand, card.rank)
          break if result[player].number_of_books_made > 0
        }
        game.advance_to_next_hand
      }
      result[player1].number_of_books_made.should == 0
      result[player2].number_of_books_made.should == 1
    end
    


  end # context
end # FishServer

