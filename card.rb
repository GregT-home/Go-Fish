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


  # Returns an array of Playing Cards based on the given strings
  # The RE splits sequences similar to: 5S 5-S 10-C 10C, etc. into three
  # elements: Whole String, Rank and Suit.
  CARD_REGEXP = /(10|[2-9]|[JQKA])\W*[of]*\W*([CHSD])/i
  def self.new_from_hand_strings(*hand_strings)
    number_of_hands = hand_strings.count
    hand_strings = hand_strings.map { |string| string = string.split }

    hand_size = hand_strings[0].count
    
    stacked_deck = []
    
    deck_array = []
    hand_size.downto(1) do |card_num| 
      hand_strings.count.times do |hand_num|
        deck_array << new_card_from_s(hand_strings[hand_num][card_num-1])
      end
    end
    deck_array.reverse
  end




  private
  # Returns an array of Playing Cards, based on a space separated string.
  def self.new_card_from_s(string)
    if rank_suit=CARD_REGEXP.match(string)
      Card.new(rank_suit[1], rank_suit[2])
    end
  end
end # Card
