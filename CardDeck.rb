class CardDeck
  attr_reader :cards

  def initialize(test_deck=[])
    @cards = []
    @books = []

    if test_deck != []
      @cards = test_deck
    else
      @cards = PlayingCard::SUITS.map { |suit| 
        PlayingCard::RANKS.map { |rank|
          PlayingCard.new(rank,suit)
        }
      }.flatten
    end
  end

  def length
    @cards.length
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

  # does this belong here? It creates a dependency on FishHand.
  def deal(number, hands)
    number = @cards.length if number == 0
    number.times {
      hands.map { |hand|
        hand.receive_card(give_card)
        }
    }
  end
  
end # CardDeck
