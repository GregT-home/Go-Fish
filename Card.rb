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

  def to_s
    "#{@rank}-#{@suit}"
  end

  # test this exhaustively
  # as_1 = Card("A", "S"); as_2 = Card("A", "S")
  # hash { as_1 => 'Wild')
  # expect(as1).to eql(as2)
  # expect(as1).to equal (as2)
  # expect(as1).to eql? (as2)
  # check Ken's slides for actual test set
  def == card
    rank == card.rank && suit == card.suit
  end
end # Card
