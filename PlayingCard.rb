class PlayingCard
  # define constants so we can use the same literal string everywhere
  RANKS = %w(2 3 4 5 6 7 8 9 10 J Q K A)
  SUITS = %w(C D H S)

  def initialize(myrank, mysuit)
    @rank = myrank.upcase
    @suit = mysuit.upcase
    raise "Invalid rank (#{myrank}) or suit (#{mysuit}) for Card" unless rank && suit
end

  def rank
    RANKS.index(@rank)
  end

  def suit
    SUITS.index(@suit)
  end

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
  def self.cards_from_string(string)
    string.split(" ").map { |card_string| 
      self.card_from_string(card_string)
    }
  end    

  private
  def self.card_from_string(string)
    if rank_suit=/\s*(10|[2-9]|[JQKA])\W*[of]*\W*([CHSD])\w*/i.match(string)
      PlayingCard.new(rank_suit[1], rank_suit[2])
    end
  end
end # PlayingCard
