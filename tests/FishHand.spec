require_relative "../PlayingCard.rb"
require_relative "../CardDeck.rb"
require_relative "../CardUtils.rb"
require_relative "../FishHand.rb"

describe FishHand, "Hand Creation and management object." do
  context "A hand can accept cards from a deck.deal." do
    before (:each) do
      @deck = CardDeck.new
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
    card.is_a?(PlayingCard).should be true
  end
end

describe FishHand, "Hand can be queried for existence of cards." do
  context "Creating a stacked deck with 'AC 2C 3C 4C 2H 2C 2S'" do
    before (:each) do
      @deck = CardDeck.new("AC 2C 3C 4C 2H 2C 2S".to_card)
      @player=FishPlayer.new
    end

    it "can tell when a rank is present or not." do
      player.hand = deck_deal(5)
    
      deck.length.should eq 52
      shuffled_deck.length.should eq 52

      deck.deal([player])
      card = player.get_next_card
    
      card.is_a?(PlayingCard).should be true

      shuffled_deck.deal([player])
      card = player.get_next_card

      card.is_a?(PlayingCard).should be true
    end
  end
end # context
end # Hand query methods
