require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"

describe Hand, "Hand Creation and management object." do
  context "A hand can accept cards from a deck." do
    before (:each) do
      @deck = Deck.new
      @hand = Hand.new
    end

    it ".count: an empty hand has a 0 length" do
      @hand.count.should eq 0
    end

    it ".receive_cards: shows a hand can receive a card." do
      card = @deck.give_card
      @hand.receive_cards(card)
      @hand.cards[0] == card
    end

    it ".receive_cards shows how many cards received." do
      starting_hand_count = @hand.count

      cards = []
      cards << @deck.give_card
      cards << @deck.give_card
      cards << @deck.give_card
      cards << @deck.give_card

      @hand.receive_cards(cards)

      @hand.count.should eq starting_hand_count + 4
    end

    it ".receive_cards: can receive multiple cards from a deck." do
      52.times { @hand.receive_cards(@deck.give_card) }

      @deck.give_card.should eq nil
      @hand.count.should eq 52

      card = @hand.give_card
      card.should_not be_nil
      card.is_a?(Card).should be true
    end
  end

  describe Hand, ".new_cards_from_s: Hand can initialized at creation." do
    it "Can create a hand with specific cards" do
      # reversing so hands will be in "human-expected" order
      @hand = Hand.new(Card.new_from_hand_strings("AC 3C 4C 2H"))
      all_cards_present = ( @hand.cards[0].rank == "A" &&
                            @hand.cards[1].rank == "3" &&
                            @hand.cards[2].rank == "4" &&
                            @hand.cards[3].rank == "2")
      all_cards_present.should eq true
    end

    context "Creating a stacked deck with 'AC 2C 3C 4C 2H 2C 2S' and 5=card hand from it." do
      before (:each) do
        @deck = Deck.new(Card.new_from_hand_strings("AC 3C 4C 2H 2C 2S 2D"))
        @hand = Hand.new
        @reference_deck_count = @deck.count
        @reference_deck_count.should eq 7

        # put all cards into the basic hand for subsequent test cases.
        @deck.count.times { @hand.receive_cards(@deck.give_card) }
      end

      it ".rank_count: can count the number of rank present in a hand." do
        @hand.rank_count('3').should eq 1
        @hand.rank_count('12').should eq 0
      end

      it ".give_matching_cards returns [] when none match" do
        cards = @hand.give_matching_cards('5')

        cards.should_not be_nil
        cards[0].is_a?(Card).should be false
        cards.should eq []
      end

      it ".give_matching_cards returns array of matched cards that are removed from hand." do
        cards = @hand.give_matching_cards('3')
        cards.should_not be_nil
        cards[0].is_a?(Card).should be true
        cards[0].rank.should eq '3'
        @hand.rank_count('3').should eql 0
      end

      it ".got_book: can detect books" do
        @hand.got_book?('2').should eq true
      end

      it ".give_matching_cards also deletes books" do
        @hand.got_book?('2').should eq true
        cards = @hand.give_matching_cards('2')
        cards.count.should eq 4
        @hand.rank_count("2").should eq 0
      end
    end # context, using stacked_deck & hand of 5
  end # Hand can be queried

  describe Hand, ".to_s:" do
    it "can display a hand as a string" do
      # reversing so hands will be in "human-expected" order
      hand = Hand.new(Card.new_from_hand_strings("AC 3C 4C 2H"))

      hand.to_s.should eq "[A-C] [3-C] [4-C] [2-H]"
    end
  end

  describe Hand, ".sort!:" do
    it "can sort a hand" do
      # reversing so hands will be in "human-expected" order
      hand = Hand.new(Card.new_from_hand_strings("AC 3C 4C 2H"))
      hand.sort!
      hand.to_s.should eq "[A-C] [4-C] [3-C] [2-H]"
    end
  end
end # Hand


