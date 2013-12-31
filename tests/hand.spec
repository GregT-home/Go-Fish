require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"

describe Hand, "Hand Creation and management object." do
  context "A hand can accept cards from a deck." do
    before (:each) do
      @deck = Deck.new
      @hand = Hand.new
    end

    it ".length: an empty hand has a 0 length" do
      @hand.length.should == 0
    end

    it ".receive_cards: shows a hand can receive a card." do
      card = @deck.give_card
      @hand.receive_cards(card)
      @hand.cards[0] == card
    end

    it ".receive_cards shows how many cards received." do
      starting_hand_length = @hand.length

      cards = []
      cards << @deck.give_card
      cards << @deck.give_card
      cards << @deck.give_card
      cards << @deck.give_card

      @hand.receive_cards(cards)

      @hand.length.should == starting_hand_length + 4
    end

    it ".receive_cards: can receive multiple cards (52 in this case) from a deck.deal." do
      52.times { @hand.receive_cards(@deck.give_card) }

      @deck.give_card.should eq nil
      @hand.length.should eq 52

      card = @hand.give_card
      card.should_not be nil
      card.is_a?(Card).should be true
    end
  end

  describe Hand, ".new_cards_from_s: Hand can be created from a string." do
    it "Can create a hand with specific cards" do
      # reversing so hands will be in "human-expected" order
      @hand = Hand.new(Card.new_cards_from_s("AC 3C 4C 2H").reverse)
      all_cards_present = ( @hand.cards[0].rank == "A" &&
                            @hand.cards[1].rank == "3" &&
                            @hand.cards[2].rank == "4" &&
                            @hand.cards[3].rank == "2")
      all_cards_present.should == true
    end

    context "Creating a stacked deck with 'AC 2C 3C 4C 2H 2C 2S' and 5=card hand from it." do
      before (:each) do
        @deck = Deck.new(Card.new_cards_from_s("AC 3C 4C 2H 2C 2S 2D"))
        @hand = Hand.new
        @reference_deck_length = @deck.length
        @reference_deck_length.should == 7

        # deal all cards out to one hand
        @deck.length.times { @hand.receive_cards(@deck.give_card) }
        @hand.length.should == @reference_deck_length
      end

      it ".got_rank?: can ask if a rank is present, or not." do
        @hand.got_rank?('3').should be true
        @hand.got_rank?('12').should be false
      end

      it ".give_matching_cards returns [] when none match" do
        cards = @hand.give_matching_cards('5')

        cards.should_not be_nil
        cards[0].is_a?(Card).should be false
        cards.should == []
      end

      it ".give_matching_cards returns array of matched cards that are removed from hand." do
        cards = @hand.give_matching_cards('3')
        cards.should_not be_nil
        cards[0].is_a?(Card).should be true
        cards[0].rank.should == '3'
        @hand.got_rank?('3').should be false
      end

      it ".got_book: can detect books" do
        @hand.got_book?('2').should == true
      end

      it ".give_matching_cards also deletes books" do
        @hand.got_book?('2').should == true
        cards = @hand.give_matching_cards('2')
        cards.length.should == 4
        @hand.got_rank?("2").should == false
      end
    end # context, using stacked_deck & hand of 5
  end # Hand can be queried

  describe Hand, ".to_s:" do
    it "can display a hand as a string" do
      # reversing so hands will be in "human-expected" order
      @hand = Hand.new(Card.new_cards_from_s("AC 3C 4C 2H").reverse)

      @hand.to_s.should eq "[A-C] [3-C] [4-C] [2-H]"
    end
  end
end # Hand


