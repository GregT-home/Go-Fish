require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"
require_relative "../game.rb"
require_relative "../result.rb"

describe Result, "Round Result creation and manipulation." do
  context "Round results need an active game." do
    before (:each) do
      @game = Game.new(1)
    end

    it "A Round Result can be created." do
      result = Result.new(@game.current_hand, 1, "3")

      result.requesting_hand.should == @game.current_hand
      result.target_hand.should == 1
      result.target_rank.should == "3"
      result.number_of_cards_received.should == 0
      result.cards_received_from.should == nil
      result.number_of_books_made.should == 0

      expect {result.requesting_hand = 1}.to raise_error
      expect {result.target_hand = 2}.to raise_error
      expect {result.target_rank = 3}.to raise_error
    end

    it "A Round Results can have its values changed." do
      result = Result.new(@game.current_hand, 1, "3")

      expect {result.requesting_hand = 1}.to raise_error
      expect {result.target_hand = 2}.to raise_error
      expect {result.target_rank = 3}.to raise_error
      result.number_of_cards_received         = 4
      result.cards_received_from              = :some_one
      result.number_of_books_made             = 5

      result.requesting_hand.should          == 0
      result.target_hand.should              == 1
      result.target_rank.should              == "3"
      result.number_of_cards_received.should == 4
      result.cards_received_from.should      == :some_one
      result.number_of_books_made.should     == 5
    end
  end #context
end # round results creation/manipulation
