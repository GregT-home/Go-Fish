require "./card.rb"
class Deck
  attr_reader :cards

  def initialize(test_deck = nil)
    @cards = []

    if test_deck
      @cards = test_deck
    else
      @cards = Card::SUITS.map do |suit| 
        Card::RANKS.map do |rank|
          Card.new(rank,suit)
        end
      end.flatten
    end
  end

  def count
    @cards.count
  end

  def ==(deck)
    @cards == deck.cards
  end

  def shuffle
    @cards.shuffle!
  end

  def give_card
    @cards.pop
  end

  def receive_card(newcard)
    @cards.unshift(newcard)
  end

end # Deck
