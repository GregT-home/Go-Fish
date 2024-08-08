require_relative "../card.rb"
require_relative "../deck.rb"

describe Deck, "Creation and basic function" do #Deck can be created, measured, shuffled, and customized." do
  context ".new by default creates a card deck" do
    deck = Deck.new
    shuffled = Deck.new

    it ".count is 52 cards." do
      expect(deck.count).to eq 52
    end

    it ".== works to compare decks." do
      expect(deck).to eq shuffled
    end

    it ".shuffle changes the order." do
      shuffled.shuffle
      expect(deck).not_to eq shuffled
    end
  end
end

describe Deck, "Cards can be given to, and received by pseudo-players." do
  context ".new creates a default card deck" do
    before (:each) do
      # create a new card deck
      @deck = Deck.new

      # pseudo-players are decks with no cards.  We can't create an empty deck
      # so we create a deck with 1 card and remove it.
      @player = Deck.new([Card.new("A","H")])
      @player.give_card
    end
    

    it ".give_card can give all 52 cards to one pseudo-player." do
      expect(@player.count).to eql 0
    end

    it ".give_card works 52 times on a standard deck and returns nil when no cards remain." do
      card = nil
      52.times {
        card = @deck.give_card
        expect(card).not_to be nil

        @player.receive_card(card)
      }
      expect(@player.count).to eql 52

      expect(@deck.count).to be 0
      expect(card).not_to be nil
    end

    it ".receive_card puts all cards back into the deck" do
      card = nil
      52.times {
        card = @player.receive_card(@deck.give_card)
        expect(card).not_to be nil
      }

    expect(@player.count).to eql 52
    expect(@deck.count).to eql 0

    card = nil
    52.times {
        card = @deck.receive_card(@player.give_card)
        expect(card).not_to be nil
      }

    expect(@player.count).to eql 0
    expect(@deck.count).to eql 52
    end
  end
end #cards can be dealt to players


