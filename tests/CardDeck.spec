require_relative "../PlayingCard.rb"
require_relative "../CardDeck.rb"

describe CardDeck, "Creation and basic function" do #Deck can be created, measured, shuffled, and customized." do
  context ".new by default creates a card deck" do
    deck = CardDeck.new
    shuffled=CardDeck.new

    it ".length is 52 cards." do
      deck.length.should eq 52
    end

    it "== works to compare decks." do
      deck.should == shuffled
    end

    it ".shuffle changes the order." do
      shuffled.shuffle
      deck.should_not == shuffled
    end
  end
end

describe CardDeck, "Cards can be given to, and received by pseudo-players." do
  context ".new creates a default card deck" do
    before (:each) do
      # create a new card deck
      @deck = CardDeck.new

      # pseudo-players are decks with no cards.  We can't create an empty deck
      # so we create a deck with 1 card and remove it.
      @player = CardDeck.new([PlayingCard.new("A","H")])
      @player.give_card
    end
    

    it ".give_card can give all 52 cards to one pseudo-player." do
      @player.length.should eql 0
    end

    it ".give_card works 52 times on a standard deck and returns nil when no cards remain." do
      card = nil
      52.times {
        card = @deck.give_card
        card.should_not be nil

        @player.receive_card(card)
      }
      @player.length.should eql 52

      @deck.length.should be 0
      card.should_not be nil
    end

    it ".receive_card should be able to put all cards back into the deck" do
      card = nil
      52.times {
        card = @player.receive_card(@deck.give_card)
        card.should_not be nil
      }

    @player.length.should eql 52
    @deck.length.should eql 0

    card = nil
    52.times {
        card = @deck.receive_card(@player.give_card)
        card.should_not be nil
      }

    @player.length.should eql 0
    @deck.length.should eql 52
    end
  end
end #cards can be dealt to players


