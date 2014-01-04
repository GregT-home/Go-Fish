require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"
require_relative "../game.rb"
require_relative "../result.rb"

describe Game, "Initial game setup." do
  context ".new for initial game setup: Create 6 random hands." do
    before (:each) do
      @number_of_test_hands = 6
      @hand_length = (@number_of_test_hands > 4) ? 5 : 7
      @game = Game.new(@number_of_test_hands)

      @game.hands.length.should be @number_of_test_hands
      @game.hands.length.times { |i|
          @game.hands[i].length.should be @hand_length
      }
    end # before (:each)
    
    it ".current_hand_index returns the index" do
      @game.current_hand_index.should eq 0
    end

    it ".advance_to_next_hand advances the index to the next player" do
      @game.advance_to_next_hand
      @game.current_hand_index.should eq 1
    end

    it ".advance_to_next_hand goes around in an ordered loop of hands." do
      first_hand = @game.current_hand_index
      @number_of_test_hands.times { @game.advance_to_next_hand }
      @game.current_hand_index.should eql first_hand
    end

  end # context for random hands
end # game setup tests

describe Game, "test typical round outcomes." do
  context "Stack a deck with with 3 known hands." do
    before (:each) do
      @test_hand_size = 7
      @number_of_test_hands = 3
      target_hand, stacked_deck = [],[]
      target_hand[0] = "2C 2H 3C QH 5C 4H 9H".split
      target_hand[1] = "2S 2D 3S 3D 5S 4D 9C".split
      target_hand[2] = "10C 10H 10S 10D AC AH 9S".split
      @test_hand_size.downto(0) { |card_num| 
        @number_of_test_hands.times { |hand_num|
          stacked_deck << target_hand[hand_num][card_num]
        }
      }

      extra_cards = "3H".split
      extra_cards.map { |card_string| stacked_deck << card_string }

      stacked_cards_string = stacked_deck.join(" ")
      @game = Game.new(@number_of_test_hands,
                       Card.new_cards_from_s(stacked_cards_string))

      @game.hands.length.should be @number_of_test_hands
      @game.hands.length.times { |i|
        @game.hands[i].length.should be @test_hand_size
      }

      # test a few samples for validity
      @game.hands[0].cards[0].should eq Card.new("Q", "H")
      @game.hands[2].cards[3].should eq Card.new("10", "C")
      @game.deck.cards[0].should eq Card.new("3", "H")
    end # before (:each)

    it ".play_round, case 1: ask Victim: none; Pond: No; Book: N/A; next player." do
      started_with = @game.hands[@game.current_hand_index].rank_count("4")

      result = @game.play_round(2, "4")  # hand 2 has no 4s, nor the pond
      result.requester.should eq 0
      result.victim.should eq 2
      result.rank.should eq "4"
      result.matches.should eq 0
      result.received_from.should eq :pond
      result.books_made.should eq 0

      @game.hands[@game.current_hand_index].rank_count("4").should eq started_with
      @game.current_hand_index.should eql 1
    end

    it ".play_round, case 2: ask Victim: gets; Pond: N/A; Book: no; plays again." do
      started_with = @game.hands[@game.current_hand_index].rank_count("3")

      result = @game.play_round(1, "3")  # hand 1 has 2 x 3s
      result.matches.should eq 2
      result.received_from.should eq 1
      result.books_made.should eq 0

      @game.hands[@game.current_hand_index].rank_count("3").should eq started_with + 2
      @game.current_hand_index.should eql 0
    end

    it ".play_round, case 3: ask Victim: gets; Pond: N/A; Book: Yes; plays again." do
      started_with = @game.hands[@game.current_hand_index].rank_count("2")

      result = @game.play_round(1, "2")  # hand 1 has 2 x 2s
      result.matches.should eq 2
      result.received_from.should eq 1
      result.books_made.should eq 1

      @game.hands[@game.current_hand_index].rank_count("2").should eq 0 # book removed from hand
      @game.current_hand_index.should eql 0

      @game.books[@game.current_hand_index][-1].should eq "2"
    end

    it ".play_round, case 4: ask Victim: no get; Pond: get; Book: no; plays again." do
      started_with = @game.hands[@game.current_hand_index].rank_count("3")

      result = @game.play_round(2, "3")  # hand 2 has no 3s, pond does
      result.matches.should eq 1
      result.received_from.should eq :pond
      result.books_made.should eq 0

      @game.hands[@game.current_hand_index].rank_count("3").should eq started_with + 1
      @game.current_hand_index.should eql 0
    end

    it ".play_round, case 5: ask Victim: no get; Pond: get; Book: yes; plays again." do
      # we play 2 hands to get to do this
      started_with = @game.hands[@game.current_hand_index].rank_count("3")
      @game.play_round(1, "3") #hand 1 has 2 x 3s (test case 2)

      result = @game.play_round(2, "3")  # hand 2 has no 3s, but pond does
      result.matches.should eq 1
      result.received_from.should eq :pond
      result.books_made.should eq 1

      @game.hands[@game.current_hand_index].rank_count("3").should eq 0
      @game.current_hand_index.should eql 0
      @game.books[@game.current_hand_index][-1].should eq "3"
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
      @game.books[0] = ["2", "K", "A"]

      book_list = "2s, As, Ks"
      @game.books_to_s(0).should eq book_list
    end

    it ".play_round: checks for end of game" do
      #take last card from deck
      card = @game.deck.give_card
      @game.deck.length.should eq 0

      next_card = @game.deck.give_card
      next_card.should be_nil

      # Play a round: ask for 3 from hand 2, don't get one, don't get from pond
      result = @game.play_round(2, "3")
      result.received_from.should be_nil
      result.matches.should eq 0
      
      result.game_over.should eq true
      @game.over?.should eq true
    end

  end # context
end # Game tests
