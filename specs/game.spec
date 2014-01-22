require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"
require_relative "../game.rb"
require_relative "../result"
require_relative "../Player.rb"
#require_relative "../fishserver.rb"
require_relative "./testhelp"
require "pry"

describe Game, "Initial game setup." do
  context "Use .new, and add_player to set up games." do
    before (:each) do
      names = %w(One Two Three Four Five Six)

      @number_of_test_players = names.count
      @hand_count = (@number_of_test_players > 4) ? 5 : 7
      @game = Game.new()

      names.each_with_index { |name, i| @game.add_player(i+10, name) }
      @game.start_game()

    end # before (:each)
    
    it "Players are set up properly" do
      @game.players.each { |player| player.hand.count.should be @hand_count }
    end

    it ".current_player is a player and the 'first' player" do
      @game.current_player.is_a?(Player).should be_true
      @game.current_player.should eql @game.players.first
    end

    it ".advance_to_next_player advances the index to the next player" do
      prev_player = @game.current_player
      @game.advance_to_next_player
      @game.current_player.should_not eq prev_player
    end

    it ".advance_to_next_player goes around in an ordered loop of players." do
      first_player = @game.current_player
      @number_of_test_players.times { @game.advance_to_next_player }
      @game.current_player.should eql first_player
    end
  end # context for random players
end # game setup tests

describe Game, ".books_to_s when books_list not initialized" do
  it ".books_to_s returns null string when no books" do
    @game = Game.new()
    @game.add_player(1, "Player Test")
    @game.books_to_s(@game.current_player).should eq ""
  end
end

describe Game, "test typical round outcomes." do
  context "Create a game with a stacked of known player hands." do
    before (:each) do
      names = %w(First Second Third)
      @number_of_test_players = names.count
      @test_hand_size = (@number_of_test_players > 4) ? 5 : 7

      test_deck = TestHelp.cards_from_hand_s( "2C 2H 3C QH 5C 4H 9H",
                                          "2S 2D 3S 3D 5S 4D 9C",
                                          "10C 10H 10S 10D AC AH 9S")
      # add an extra card
      test_deck.unshift(Card.new("3", "H"))

      @game = Game.new()
      names.each_with_index { |name, i| @game.add_player(i+20, name) }
      @game.start_game(test_deck)
    end # before (:each)

    it "Test Deck results in expected hands." do
      @game.number_of_players.should be @number_of_test_players
      @game.players.each { |player| player.hand.count.should be @test_hand_size }

      # test a few samples for validity
      @game.players[0].hand.cards[0].should eq Card.new("Q", "H")
      @game.players[2].hand.cards[3].should eq Card.new("10", "C")
      @game.deck.cards[0].should eq Card.new("3", "H")
    end

    it ".play_round, case 1: ask Victim: none; Pond: No; Book: N/A; next player." do
      start_player = @game.current_player
      started_with = start_player.hand.rank_count("4")

      result = @game.play_round(@game.players[2], "4")  # hand 2 has no 4s, nor the pond

      result.requester.should eq start_player
      result.victim.should eq @game.players[2]
      result.rank.should eq "4"
      result.matches.should eq 0
      result.received_from.should eq :pond
      result.books_made.should eq 0

      @game.current_player.should_not eql start_player
    end

    it ".play_round, case 2: ask Victim: gets; Pond: N/A; Book: no; plays again." do
      start_player = @game.current_player
      started_with = start_player.hand.rank_count("3")

      result = @game.play_round(@game.players[1], "3")  # hand 1 has 2 x 3s
      result.matches.should eq 2
      result.received_from.should eq @game.players[1]
      result.books_made.should eq 0

      @game.current_player.hand.rank_count("3").should eq started_with + 2
      @game.current_player.should eql start_player
    end

    it ".play_round, case 3: ask Victim: gets; Pond: N/A; Book: Yes; plays again." do
      starting_player = @game.current_player
      started_with = starting_player.hand.rank_count("2")

      result = @game.play_round(@game.players[1], "2")  # hand 1 has 2 x 2s
      result.matches.should eq 2
      result.received_from.should eq @game.players[1]
      result.books_made.should eq 1

      @game.current_player.hand.rank_count("2").should eq 0 # book removed from hand
      @game.current_player.should eq starting_player
      @game.books(@game.current_player).should include("2")
    end

    it ".play_round, case 4: ask Victim: no get; Pond: get; Book: no; plays again." do
      starting_player = @game.current_player
      started_with = starting_player.hand.rank_count("3")

      result = @game.play_round(@game.players[2], "3")  # hand 2 has no 3s, pond does
      result.matches.should eq 1
      result.received_from.should eq :pond
      result.books_made.should eq 0

      @game.current_player.hand.rank_count("3").should eq started_with + 1
      @game.current_player.should eq starting_player
    end

    it ".play_round, case 5: ask Victim: no get; Pond: get; Book: yes; plays again." do
      # we play 2 hands to get to do this
      starting_player = @game.current_player
      started_with = starting_player.hand.rank_count("3")
      @game.play_round(@game.players[1], "3") #hand 1 has 2 x 3s (test case 2)

      result = @game.play_round(@game.players[2], "3")  # hand 2 has no 3s, but pond does
      result.matches.should eq 1
      result.received_from.should eq :pond
      result.books_made.should eq 1

      @game.current_player.hand.rank_count("3").should eq 0
      @game.current_player.should eq starting_player
      @game.books(@game.current_player).should include("3")
    end

    it ".play_round, case 6: ask Victim: no get; Pond: get; Book: yes-surprise; next player." do
      # we play 2 hands to get to do this
      starting_player = @game.current_player
      started_with = starting_player.hand.rank_count("3")
      @game.play_round(@game.players[1], "3") #hand 1 has 2 x 3s (test case 2)

      result = @game.play_round(@game.players[2], "Q")  # hand 2 has no Qs, pond has a 3 for book
      result.matches.should eq 0
      result.received_from.should eq :pond
      result.books_made.should eq 1
      @game.current_player.hand.rank_count("3").should eq 0
      @game.current_player.should_not eql starting_player
      @game.books(starting_player).should include("3")
    end

    it ".play_round logic to check for books in initial hands" do
      expected_result = [0, 0, 1] # 1st two players have none, third has 1

      @game.players.each_with_index do |player, i|
        player.hand.cards.each_with_index do |card, i|
          if @game.process_books(card.rank) != 0
            result.books_made.should eq expected_result[i]
            break
          end
        end
      end
    end

    it ".books_to_s returns null string when no books" do
      @game.books_to_s(@game.current_player).should eq  ""
    end

    it ".books_to_s can display a list of books" do
      # Remove any matching cards from the current hand
      @game.current_player.hand.give_matching_cards("2")
      @game.current_player.hand.give_matching_cards("K")
      @game.current_player.hand.give_matching_cards("A")

      # Stack the hand with three books
      cards = TestHelp.cards_from_hand_s("2C 2S 2D 2H KC KS KD KH AC AS AD AH")
      @game.current_player.hand.receive_cards(cards)

      # check the hand for each kind of book
      @game.process_books("2").should eql 1
      @game.process_books("K").should eql 1
      @game.process_books("A").should eql 1

      book_list = "2s, As, Ks"
      @game.books_to_s(@game.current_player).should eq book_list
    end

    it ".play_round: checks for end of game" do
      #take last card from deck
      card = @game.deck.give_card
      @game.deck.count.should eq 0

      next_card = @game.deck.give_card
      next_card.should be_nil

      # Play a round: ask for 3 from hand 2, don't get one, don't get from pond
      result = @game.play_round(@game.players[2], "3")
      result.received_from.should be_nil
      result.matches.should eq 0
      
      result.game_over.should eq true
      @game.over?.should eq true
    end

  end # context
end # Game tests

describe Game, ".end_game" do

  Hand_str_regexp = Regexp.new("\[|10|[2-9]|[JQKA]|-[CDHS]]", true)

  context "Create a basic game game." do
    before (:each) do
      @game = Game.new()
      @game.add_player(501, "One")
      @game.start_game()

      @current_player = @game.current_player
    end
    
    it "#new: creates the game" do
      @game.is_a?(Game).should be true
    end

    it "#add_player: adds a new player" do
      @game.players[0].is_a?(Player).should be true
    end

    it ".started is true if the game is started" do
      expect(@game.started).to eq true
    end

    it ".start_game returns nil if game is already started" do
      result = @game.start_game
      expect(result).to eq nil
    end

    it ".add_player returns nil if game is started" do
      result = @game.add_player(1, "A Player")
      expect(result).to eq nil
    end
  end

  context ".endgame" do
    before (:each) do
      names = %w(One Two Three)
      @game = Game.new()
      names.each_with_index do |name, i|
        @game.add_player(40 + i, name)
        @game.current_player.messages(true) #consume "Waiting for.." message
      end
      
      @game.start_game()

      @current_player = @game.current_player
    end

    it ".endgame: can handle a single winner" do
      # Player 0 gets 1 x book, Player 1 gets 3, Player 2 gets 2
      @game.books_list[@game.players[0]] << "2"
      @game.books_list[@game.players[1]] << "4" << "5" << "A"
      @game.books_list[@game.players[2]] << "8" << "9"

      @game.endgame

      messages = @game.players[0].messages(true)
#      msg.should =~ Hand_str_regexp

      target_msg =<<-EOF
=========================
There are no more fish in the pond.  Game play is over.
Here is the final outcome:
EOF
      messages[0].should =~ Regexp.new(target_msg.strip)
      messages[1].should =~ Regexp.new(".*Player \\d+, One, made 1 books \\(2s\\)")
      messages[2].should =~ Regexp.new("Player \\d+, Two, made 3 books \\(4s, 5s, As\\) and is the winner\\!")
      messages[3].should =~ Regexp.new(".*Player \\d+, Three, made 2 books \\(8s, 9s\\)")
    end
    
  it ".endgame: can handle a tie" do
      # Player 0 gets 1 x book, Player 1 gets 3, Player 2 gets 2
      @game.books_list[@game.players[0]] << "2"
      @game.books_list[@game.players[1]] << "4" << "5" << "A"
      @game.books_list[@game.players[2]] << "8" << "9" << "K"

      @game.endgame

      messages = @game.players[0].messages(true)

#      msg.should =~ Hand_str_regexp

      target_msg =<<-EOF
=========================
There are no more fish in the pond.  Game play is over.
Here is the final outcome:
EOF
      messages[0].should =~ Regexp.new(target_msg.strip)
      messages[1].should =~ Regexp.new(".*Player \\d+, One, made 1 books \\(2s\\)")
      messages[2].should =~ Regexp.new("Player \\d+, Two, made 3 books \\(4s, 5s, As\\) and ties for the win\\!")
      messages[3].should =~ Regexp.new(".*Player \\d+, Three, made 3 books \\(8s, 9s, Ks\\) and ties for the win\\!")
    end
   end # context
end # .end_game

describe Game, "." do
  context "(null) Create test hands + players." do
    before (:each) do
      names = %w(One Two Three)
      @game = Game.new()
      names.each_with_index do |name, i|
        @game.add_player(100 + i, name)
        @game.current_player.messages(true) #consume "Waiting for.." message
      end

      @game.start_game()

      @current_player = @game.current_player
    end # before each

    it ".give_all_players_status: can display multiple player status" do
      @game.books_list[@game.players[1]] = ["2", "7", "Q"]
      @game.books_list[@game.players[2]] = ["A"]

      @game.give_player_status(@game.players[0])
      messages = @game.players[0].messages(true)
      messages[0].should =~ Regexp.new("One \\(#\\d+\\) has 7 cards and has made 0 books \(\)")
      messages[1].should =~ Regexp.new("Two \\(#\\d+\\) has 7 cards and has made 3 books \\(2s, 7s, Qs\\)")
      messages[2].should =~ Regexp.new("Three \\(#\\d+\\) has 7 cards and has made 1 books \\(As\\)")
    end

    it ".calculate_rankings: it determines player ranking" do
      # Player 1 wins, Player 2 comes second, 0 is third
      @game.books_list[@game.players[1]] = ["Q", "2", "7"]
      @game.books_list[@game.players[2]] = ["A"]

      rank_list = @game.calculate_rankings
      rank_list.should eq [2, 0, 1]
    end

    it ".calculate_rankings: it shows ties" do

      # Players 1 & 2 both have 2
      @game.books_list[@game.players[1]] = ["Q", "2"]
      @game.books_list[@game.players[2]] = ["7", "A"]

      rank_list = @game.calculate_rankings
      rank_list.should eq [1, 0, 0]
    end

    it ".parse_ask can split raw input into player and rank" do
      player_num, rank = @game.parse_ask("ask 1 for 3s")
      player_num.should eq 1
      rank.should eq "3"

      player_num, rank = @game.parse_ask("ask 1 3")
      player_num.should eq 1
      rank.should eq "3"

      player_num, rank = @game.parse_ask("ask Player 1, have any 3s?")
      player_num.should eq 1
      rank.should eq "3"
    end

    it ".process_commands: prints help when it does not understand" do
      type = @game.process_commands(@current_player, "hello")
      
      type.should eq :private

      message = @current_player.messages[0].strip
      message.should =~ Regexp.new("Not understood.*")

     end
 
   it ".process_commands: understands deck size and shows it" do
      type = @game.process_commands(@current_player, "deck size")
      
      type.should eq :private
      message = @current_player.messages[0].strip
      message.should =~ Regexp.new("\\d+ card.* are left in the pond")
     end

   it ".process_commands: understands hand and prints cards" do
      type = @game.process_commands(@current_player, "hand")
      
      type.should eq :private

      test_regexp = Hand_str_regexp

      message = @current_player.messages[0].strip
      message.should =~ test_regexp
     end

   it ".process_commands: understands status and shows it" do
      type = @game.process_commands(@current_player, "status")
      
      type.should eq :private

      message = @current_player.messages[0].strip
      message.should =~ Regexp.new(".*has \\d+ cards and has made \\d+ book.*")
     end

   it ".process_commands: understands well-formed ask and processes it" do
      type = @game.process_commands(@current_player,
                                    "ask #{@game.players[2].number} for 3s")
      
      message = @current_player.messages[0].strip
      message.should =~ Regexp.new(".*(player .*)asked for .* from player #.*")
      type.should eq :public
     end

   it ".process_commands: understands well-formed ask with invalid player and processes it" do
      type = @game.process_commands(@current_player, "ask 4 for 3s")
      
      message = @current_player.messages[0].strip
      message.should =~ Regexp.new("That player does not exist.")

      type.should eq :private

      type = @game.process_commands(@current_player, "ask 10 for 3s")
      
      message = @current_player.messages[0].strip
      message.should =~ Regexp.new("That player does not exist.")

      type.should eq :private

     end

   it ".process_commands: handles badly-formed ask properly" do
      type = @game.process_commands(@current_player, "ask feep for 3s")
      
      type.should eq :private

      test_msg = "Victim and/or rank not recognized."
      message = @current_player.messages[0].strip
      message.should eq test_msg
     end

   it ".process_commands: does not allow non-existent players to be asked" do
      type = @game.process_commands(@current_player, "ask 5 for 3s")
      
      type.should eq :private

      test_msg = "That player does not exist."
      message = @current_player.messages[0].strip
      message.should eq test_msg
     end
  end
end

