require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"
require_relative "../game.rb"
require_relative "../result.rb"

describe Game, "Initial game setup." do
  context ".new for initial game setup: Create 6 random hands." do
    before (:each) do
      @number_of_test_hands = 6
      @hand_count = (@number_of_test_hands > 4) ? 5 : 7
      @game = Game.new(@number_of_test_hands)
    end # before (:each)
    
    it ".new sets up properly" do
      @game.hands.count.should be @number_of_test_hands
      @game.hands.each { |hand| hand.count.should be @hand_count }
    end

    it ".current_hand is a hand and the 'first' hand" do
      @game.current_hand.is_a?(Hand)
      @game.current_hand.should eql @game.hands.first
    end

    it ".advance_to_next_hand advances the index to the next player" do
      prev_hand = @game.current_hand
      @game.advance_to_next_hand
      @game.current_hand.should_not eq prev_hand
      @game.current_hand.should_not eq @game.hands
    end

    it ".advance_to_next_hand goes around in an ordered loop of hands." do
      first_hand = @game.current_hand
      @number_of_test_hands.times { @game.advance_to_next_hand }
      @game.current_hand.should eql first_hand
    end

  end # context for random hands
end # game setup tests

describe Game, "test typical round outcomes." do
  context "Create a game with a stacked of known hands." do
    before (:each) do
      @test_hand_size = 7
      @number_of_test_hands = 3
      test_deck = Card.new_from_hand_strings( "2C 2H 3C QH 5C 4H 9H",
                                          "2S 2D 3S 3D 5S 4D 9C",
                                          "10C 10H 10S 10D AC AH 9S")
      # add an extra card
      test_deck.unshift(Card.new("3", "H"))

      @game = Game.new(@number_of_test_hands, test_deck)

    end # before (:each)

    it "Test Deck results in expected hands." do
      @game.hands.count.should be @number_of_test_hands
      @game.hands.count.times { |i|
        @game.hands[i].count.should be @test_hand_size
      }

      # test a few samples for validity
      @game.hands[0].cards[0].should eq Card.new("Q", "H")
      @game.hands[2].cards[3].should eq Card.new("10", "C")
      @game.deck.cards[0].should eq Card.new("3", "H")
    end

    it ".play_round, case 1: ask Victim: none; Pond: No; Book: N/A; next player." do
      start_hand = @game.current_hand
      started_with = start_hand.rank_count("4")

      result = @game.play_round(@game.hands[2], "4")  # hand 2 has no 4s, nor the pond

      result.requester.should eq start_hand
      result.victim.should eq @game.hands[2]
      result.rank.should eq "4"
      result.matches.should eq 0
      result.received_from.should eq :pond
      result.books_made.should eq 0

      @game.current_hand.should_not eql start_hand
    end

    it ".play_round, case 2: ask Victim: gets; Pond: N/A; Book: no; plays again." do
      started_with = @game.current_hand.rank_count("3")

      result = @game.play_round(@game.hands[1], "3")  # hand 1 has 2 x 3s
      result.matches.should eq 2
      result.received_from.should eq @game.hands[1]
      result.books_made.should eq 0

      @game.current_hand.rank_count("3").should eq started_with + 2
      @game.current_hand.should eql @game.hands.first
    end

    it ".play_round, case 3: ask Victim: gets; Pond: N/A; Book: Yes; plays again." do
      starting_hand = @game.current_hand
      started_with = @game.current_hand.rank_count("2")

      result = @game.play_round(@game.hands[1], "2")  # hand 1 has 2 x 2s
      result.matches.should eq 2
      result.received_from.should eq @game.hands[1]
      result.books_made.should eq 1

      @game.current_hand.rank_count("2").should eq 0 # book removed from hand
      @game.current_hand.should eq @game.hands.first
      
#obs      @game.books[@game.current_index].should eq ["2"]

      @game.books(starting_hand).should include("2")
    end

    it ".play_round, case 4: ask Victim: no get; Pond: get; Book: no; plays again." do
      started_with = @game.current_hand.rank_count("3")

      result = @game.play_round(@game.hands[2], "3")  # hand 2 has no 3s, pond does
      result.matches.should eq 1
      result.received_from.should eq :pond
      result.books_made.should eq 0

      @game.current_hand.rank_count("3").should eq started_with + 1
      @game.current_hand.should eq @game.hands.first
    end

    it ".play_round, case 5: ask Victim: no get; Pond: get; Book: yes; plays again." do
      # we play 2 hands to get to do this
      started_with = @game.current_hand.rank_count("3")
      @game.play_round(@game.hands[1], "3") #hand 1 has 2 x 3s (test case 2)

      result = @game.play_round(@game.hands[2], "3")  # hand 2 has no 3s, but pond does
      result.matches.should eq 1
      result.received_from.should eq :pond
      result.books_made.should eq 1

      @game.current_hand.rank_count("3").should eq 0
      @game.current_hand.should eq @game.hands.first
      @game.books(@game.current_hand).should include("3")
    end

    it ".play_round, case 6: ask Victim: no get; Pond: get; Book: yes-surprise; next player." do
      # we play 2 hands to get to do this
      started_with = @game.current_hand.rank_count("3")
      starting_hand = @game.current_hand
      @game.play_round(@game.hands[1], "3") #hand 1 has 2 x 3s (test case 2)

      result = @game.play_round(@game.hands[2], "Q")  # hand 2 has no Qs, pond has a 3 for book
      result.matches.should eq 0
      result.received_from.should eq :pond
      result.books_made.should eq 1
      @game.current_hand.rank_count("3").should eq 0
      @game.current_hand.should_not eql starting_hand
      @game.books(starting_hand).should include("3")
    end

    it ".play_round logic to check for books in initial hands" do

      expected_result = [0, 0, 1]

      @game.hands.each_with_index { |hand, i|
        hand.cards.each_with_index { |card, i|
          if @game.process_books(card.rank) != 0
            result.books_made.should eq expected_result[i]
            break
          end
        }
      }
    end

    it ".books_to_s can display a list of books" do
      # Remove any matching cards from the current hand
      @game.current_hand.give_matching_cards("2")
      @game.current_hand.give_matching_cards("K")
      @game.current_hand.give_matching_cards("A")

      # Stack the hand with three books
      cards = Card.new_from_hand_strings("2C 2S 2D 2H KC KS KD KH AC AS AD AH")
      @game.current_hand.receive_cards(cards)

      # check the hand for each kind of book
      @game.process_books("2").should eql 1
      @game.process_books("K").should eql 1
      @game.process_books("A").should eql 1

      book_list = "2s, As, Ks"
      @game.books_to_s(@game.current_hand).should eq book_list
    end

    it ".play_round: checks for end of game" do
      #take last card from deck
      card = @game.deck.give_card
      @game.deck.count.should eq 0

      next_card = @game.deck.give_card
      next_card.should be_nil

      # Play a round: ask for 3 from hand 2, don't get one, don't get from pond
      result = @game.play_round(@game.hands[2], "3")
      result.received_from.should be_nil
      result.matches.should eq 0
      
      result.game_over.should eq true
      @game.over?.should eq true
    end

  end # context
end # Game tests
