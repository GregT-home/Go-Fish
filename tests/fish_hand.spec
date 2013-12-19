require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../fish_hand.rb"

describe FishHand, "Hand Creation and management object." do
  context "A hand can accept cards from a deck.deal." do
    before (:each) do
      @deck = Deck.new
      @hand=FishHand.new
    end

    it "One hand can receives all 52 cards from a deck.deal." do

      @deck.deal(0, [@hand])
      @hand.length.should eq 52
    end

    it "One hand receives all 52 cards one at a time." do
      52.times { @hand.receive_card(@deck.give_card) }

      @deck.give_card.should eq nil
      @hand.length.should eq 52

      card = @hand.give_card
      card.should_not be nil
      card.is_a?(Card).should be true
    end
  end

  describe FishHand, "Hand can be created and queried for existence of cards." do
    it "Can create a hand with specific cards" do
      # reversing so hands will be in "human-expected" order
      @hand = FishHand.new(Card.new_cards_from_string("AC 3C 4C 2H").reverse)
      all_cards_present = ( @hand.cards[0].rank == "A" &&
                            @hand.cards[1].rank == "3" &&
                            @hand.cards[2].rank == "4" &&
                            @hand.cards[3].rank == "2")
      all_cards_present.should == true
    end

    context "Creating a stacked deck with 'AC 2C 3C 4C 2H 2C 2S' and 5-card hand" do
      before (:each) do
        @deck = Deck.new(Card.new_cards_from_string("AC 3C 4C 2H 2C 2S 2D"))
        @hand = FishHand.new
        @reference_deck_length = @deck.length
        @reference_deck_length.should == 7

        @deck.deal(5, [@hand])
        @deck.length.should eq @reference_deck_length - 5
        
      end

      it "can ask if a rank is present, or not." do
        @hand.got_rank?('3').should be true
        @hand.got_rank?('10').should be false
      end

      it "can delete a card with a given rank." do
        cards = @hand.give_matching_cards('3')
        cards.should_not be_nil
        cards[0].is_a?(Card).should be true
        cards[0].rank.should == '3'
      end

      it "can detect books" do
        @deck.deal(0, [@hand])
        @hand.length.should == @reference_deck_length
        @hand.got_book?('2').should == true
      end

      it "can delete books" do
        @deck.deal(0, [@hand])
        @hand.length.should == @reference_deck_length
        @hand.got_book?('2').should == true
        cards = @hand.give_matching_cards('2')
        cards.length.should == 4
        @hand.got_rank?("2").should == false
      end
    end # context, using stacked_deck & hand of 5
  end # Hand can be queried
end # Hand query methods
