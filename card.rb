class Card
  attr_reader :rank, :suit

  # define constants so we can use the same literal string everywhere
  RANKS = %w(2 3 4 5 6 7 8 9 10 J Q K A)
  SUITS = %w(C D H S)

  def initialize(myrank, mysuit)
    @rank = myrank
    @suit = mysuit
end

  def value
    RANKS.index(@rank)
  end

  # def suit_value
  #   SUITS.index(@suit)
  # end

  def to_s
    "#{@rank}-#{@suit}"
  end

  def ==(card)
    rank == card.rank && suit == card.suit
  end

  # Returns Playing Cards based on the given string
  # The RE splits sequences similar to: 5S 5-S 10-C 10C, etc. into three
  # elements: Whole String, Rank and Suit.

  # Returns an array of Playing Cards, based on a space separated string.
  def self.new_cards_from_s(string)
    string.split(" ").map { |card_s| 
      self.new_card_from_s(card_s)
    }.reverse
  end    

  private
  def self.new_card_from_s(string)
    if rank_suit=/\s*(10|[2-9]|[JQKA])\W*[of]*\W*([CHSD])\w*/i.match(string)
      Card.new(rank_suit[1], rank_suit[2])
    end
  end
end # Card
