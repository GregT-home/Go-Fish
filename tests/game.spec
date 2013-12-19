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
      @number_of_test_hands = 6
      target_hand, tmp_deck = [],[]
      target_hand[0] = "2C 2H 3C 3H 4C 4H".split
      target_hand[1] = "2S 2D 3S 3D 4S 4D".split
      target_hand[2] = "5S 5D 6S 6D 7S 7D".split
      target_hand[3] = "5C 5H 6C 6H 7C 7H".split
      target_hand[4] = "10S 10D JS JD AS AD".split
      target_hand[5] = "10C 10H JC JH AC AH".split

      stacked_cards_string = target_hand.each { |hand|
        hand.each { |card|
          tmp_deck << card
        }
      }.flatten.join(" ")

      @game = Game.new(@number_of_test_hands,
                       Card.new_cards_from_s(stacked_cards_string))

      @game.hands.length.should be 6
      @game.hands.length.times { |i|
      @game.hands[i].length.should be 6
      }
    end # before (:each)

    it "fish_the_deck: ask the deck for a card and get it." do
    end


    it "play_round: Hand X asks Hand Y for rank Z and gets none." do
      pending ("Test waiting for completion of ask method")
      result = @game.play_round(0, 1, "6")
      result.should_not be_nil

      result.requesting_hand.should == 0
      result.target_hand.should == 1
      result.target_rank.should == "6"
      result.number_of_cards_received.should == 0
      result.number_of_books_made.should == 0
    end

    it "play_round: Hand X asks Hand Y for Rank Z and gets them.)." do
      pending ("Test waiting for completion of ask method")
      result = @game.play_round(0, 1, "6")
      result.should_not be_nil

      result.requesting_hand.should == 0
      result.target_hand.should == 1
      result.target_rank.should == "6"
      result.number_of_cards_received.should == 0
      result.number_of_books_made.should == 0
    end


    
  end # context
end # Hand tests
