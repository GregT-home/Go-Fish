require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"
require_relative "../game.rb"
require_relative "../result.rb"

describe Game, "Initial game setup." do
  context "Initial game setup: Create game with 6 random hands." do
    before (:each) do
      @number_of_test_hands = 6
      @game = Game.new(@number_of_test_hands)

      @game.hands.length.should be 6
      @game.hands.length.times { |i|
        @game.hands[i].length.should be 6
      }
    end # before (:each)
    
    it "We know the current hand" do
      @game.current_hand.should == 0
    end

    it "We can advance to the next player" do
      @game.advance_to_next_hand
      @game.current_hand.should == 1
    end

    it "When we get to the end of the list, we advance to the first hand" do
      first_hand = @game.current_hand
      @number_of_test_hands.times { @game.advance_to_next_hand }
      @game.current_hand.should eql first_hand
    end

  end # context for random hands
end # game setup tests

describe Game, "Play typical rounds." do
  context "Create a game with 6 known hands." do
    before (:each) do
      @hand_size = 6
      @number_of_test_hands = 6
      target_hand, stacked_deck = [],[]
      target_hand[0] = "2C 2H 3C QH 5C 4H".split
      target_hand[1] = "2S 2D 3S 3D 5S 4D".split
      target_hand[2] = "4S 5D 6S 6D 7S 7D".split
      target_hand[3] = "4C 5H 6C 6H 7C 7H".split
      target_hand[4] = "10S 10D JS JD AS AD".split
      target_hand[5] = "10C 10H JC JH AC AH".split
      @hand_size.downto(0) { |card_num| 
        @number_of_test_hands.times { |hand_num|
          stacked_deck << target_hand[hand_num][card_num]
        }
      }
      extra_cards = "3H".split
      extra_cards.map { |card_string|
        stacked_deck << card_string
      }
      stacked_cards_string = stacked_deck.join(" ")

      @game = Game.new(@number_of_test_hands,
                       Card.new_cards_from_s(stacked_cards_string))

      @game.hands.length.should be @number_of_test_hands
      @game.hands.length.times { |i|
        @game.hands[i].length.should be @hand_size
      }

      # test a few samples for validity
      @game.hands[0].cards[3].should == Card.new("Q", "H")
      @game.hands[5].cards[0].should == Card.new("10", "C")
      @game.deck.cards[0].should == Card.new("3", "H")
    end # before (:each)

    it "#ask_hand_for_card: does not get it; resulting # of cards is 0." do
      result = @game.ask_hand_for_card(@game.hands[1],"8")
      result.number_of_cards_received.should == 0
      result.cards_received_from.should == nil
    end

    it "#ask_hand_for_card: gets it; resulting # of cards is 1, cards removed from target hand." do
      hand0_count = @game.hands[0].cards.length
      hand1_count = @game.hands[1].cards.length

      result = @game.ask_hand_for_card(@game.hands[1],"5")
      result.number_of_cards_received.should == 1
      result.cards_received_from.should == @game.hands[1]

      @game.hands[0].cards.length.should == hand0_count + 1
      @game.hands[1].cards.length.should == hand1_count - 1
    end

    it "#ask_hand_for_card: gets > 1; resulting # of cards reflects # received." do
      hand0_count = @game.hands[0].cards.length
      hand1_count = @game.hands[1].cards.length

      result = @game.ask_hand_for_card(@game.hands[1],"2")
      result.number_of_cards_received.should == 2
      result.cards_received_from.should == @game.hands[1]

      @game.hands[0].cards.length.should == hand0_count + 2
      @game.hands[1].cards.length.should == hand1_count - 2
    end

    it "play_round: 1) Player->Victim: none; Pile: Yes; Book: N/A; turn over." do
      result = @game.play_round(@game.hands[1], "6")  # hand 1 has no 6s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "6"
      result.number_of_cards_received.should == 1
      result.cards_received_from.should == :deck
      result.number_of_books_made.should == 0

      @game.advance_to_next_hand
      @game.current_hand.should eql 1
    end

    it "play_round: 2) Player->Victim: gets; Pile: N/A; Book: N/A; plays again." do
      result = @game.play_round(@game.hands[1], "3")  # hand 1 has 2 x 3s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "3"
      result.number_of_cards_received.should == 2
      result.cards_received_from.should == @game.hands[1]
      result.number_of_books_made.should == 0

      @game.current_hand.should eql 0
    end

    it "play_round: 3( Player->Victim: gets; Pile: N/A; Book: Yes; plays again." do
      result = @game.play_round(@game.hands[1], "2")  # hand 1 has 2 x 2s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "2"
      result.number_of_cards_received.should == 2
      result.cards_received_from.should == @game.hands[1]
      result.number_of_books_made.should == 1

      @game.current_hand.should eql 0
    end

    it "play_round: 4) Player->Victim: no get; Pile: get; Book: no; plays again." do
      result = @game.play_round(@game.hands[1], "8")  # hand 1 has no 8s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "8"
      result.number_of_cards_received.should == 1
      result.cards_received_from.should == :deck
      result.number_of_books_made.should == 0

      @game.current_hand.should eql 0
    end

    it "play_round: 5) Player->Victim: no get; Pile: get; Book: yes; plays again." do
      result = @game.play_round(@game.hands[1], "8")  # hand 1 has no 8s
      result.requesting_hand.should == @game.hands[0]
      result.target_hand.should == @game.hands[1]
      result.target_rank.should == "8"
      result.number_of_cards_received.should == 1
      result.cards_received_from.should == :deck
      result.number_of_books_made.should == 0

      @game.current_hand.should eql 0
    end


    


    # it "play_round: Hand X asks Hand Y for Rank Z and gets them.)." do
    #   pending ("Test waiting for completion of ask method")
    #   result = @game.play_round(0, 1, "6")
    #   result.should_not be_nil

    #   result.requesting_hand.should == 0
    #   result.target_hand.should == 1
    #   result.target_rank.should == "6"
    #   result.number_of_cards_received.should == 0
    #   result.number_of_books_made.should == 0
    # end


    
  end # context
end # Hand tests
