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
      result = Result.new(@game.current_hand_index, 1, "3")

      result.requester.should == @game.current_hand_index
      result.victim.should == 1
      result.rank.should == "3"
      result.matches.should == 0
      result.received_from.should == nil
      result.number_of_books_made.should == 0
      result.game_over.should == false

      expect {result.requester = 1}.to raise_error
      expect {result.victim = 2}.to raise_error
      expect {result.rank = 3}.to raise_error
    end

    it "A Round Results can have its values changed." do
      result = Result.new(@game.current_hand_index, 1, "3")

      expect {result.requester = 1}.to raise_error
      expect {result.victim = 2}.to raise_error
      expect {result.rank = 3}.to raise_error
      result.matches                          = 4
      result.received_from                    = :some_one
      result.number_of_books_made             = 5
      result.game_over                        = 6

      result.requester.should                == 0
      result.victim.should                   == 1
      result.rank.should                     == "3"
      result.matches.should                  == 4
      result.received_from.should            == :some_one
      result.number_of_books_made.should     == 5
      result.game_over.should                == 6
    end
  end #context
end # round results creation/manipulation
