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

  # test this exhaustively
  # as_1 = Card("A", "S"); as_2 = Card("A", "S")
  # hash { as_1 => 'Wild')
  # assert(as1 == as2)
  # assert(as1 equal as2)
  # assert (as1 eql? as2)
  # check Ken's slides for actual test set
  def == card
    rank == card.rank && suit == card.suit
  end
end # Card
