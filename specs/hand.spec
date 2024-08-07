require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"
require_relative "./testhelp.rb"

describe Hand, "Hand Creation and management object." do
  context "A hand can accept cards from a deck." do
    before (:each) do
      @deck = Deck.new
      @hand = Hand.new
    end

    it ".count: an empty hand has a 0 length" do
      expect(@hand.count).to eq 0
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

      expect(@hand.count).to eq starting_hand_count + 4
    end

    it ".receive_cards: can receive multiple cards from a deck." do
      52.times { @hand.receive_cards(@deck.give_card) }

      expect(@deck.give_card).to be nil
      expect(@hand.count).to eq 52

      card = @hand.give_card
      expect(card).not_to be nil
      expect(card.is_a?(Card)).to be true
    end
  end

  describe Hand, ".new_cards_from_s: Hand can initialized at creation." do
    it "Can create a hand with specific cards" do
      # reversing so hands will be in "human-expected" order
      @hand = Hand.new(TestHelp.cards_from_hand_s("AC 3C 4C 2H"))
      all_cards_present = ( @hand.cards[0].rank == "A" &&
                            @hand.cards[1].rank == "3" &&
                            @hand.cards[2].rank == "4" &&
                            @hand.cards[3].rank == "2")
      expect(all_cards_present).to be true
    end

    context "Creating a stacked deck with 'AC 2C 3C 4C 2H 2C 2S' and 5=card hand from it." do
      before (:each) do
        @deck = Deck.new(TestHelp.cards_from_hand_s("AC 3C 4C 2H 2C 2S 2D"))
        @hand = Hand.new
        @reference_deck_count = @deck.count
        expect(@reference_deck_count).to eq 7

        # put all cards into the basic hand for subsequent test cases.
        @deck.count.times { @hand.receive_cards(@deck.give_card) }
      end

      it ".rank_count: can count the number of rank present in a hand." do
        expect(@hand.rank_count('3')).to eq 1
        expect(@hand.rank_count('12')).to eq 0
      end

      it ".give_matching_cards returns [] when none match" do
        cards = @hand.give_matching_cards('5')

        expect(cards).not_to be nil
        expect(cards[0].is_a?(Card)).to be false
        expect(cards).to eq []
      end

      it ".give_matching_cards returns array of matched cards that are removed from hand." do
        cards = @hand.give_matching_cards('3')
        expect(cards).not_to be nil
        expect(cards[0].is_a?(Card)).to be true
        expect(cards[0].rank).to eq '3'
        expect(@hand.rank_count('3')).to eql 0
      end

      it ".got_book: can detect books" do
        expect(@hand.got_book?('2')).to eq true
      end

      it ".give_matching_cards also deletes books" do
        expect(@hand.got_book?('2')).to be true
        cards = @hand.give_matching_cards('2')
        expect(cards.count).to eq 4
        expect(@hand.rank_count("2")).to eq 0
      end
    end # context, using stacked_deck & hand of 5
  end # Hand can be queried

  describe Hand, ".to_s:" do
    it "can display a hand as a string" do
      # reversing so hands will be in "human-expected" order
      hand = Hand.new(TestHelp.cards_from_hand_s("AC 3C 4C 2H"))

      expect(hand.to_s).to eq "[A-C] [3-C] [4-C] [2-H]"
    end
  end

  describe Hand, ".sort!:" do
    it "can sort a hand" do
      # reversing so hands will be in "human-expected" order
      hand = Hand.new(TestHelp.cards_from_hand_s("AC 3C 4C 2H"))
      hand.sort!
      expect(hand.to_s).to eq "[A-C] [4-C] [3-C] [2-H]"
    end
  end
end # Hand


