class TestHelp
  # Returns an array of Playing Cards based on the given strings
  # The RE splits sequences similar to: 5S 5-S 10-C 10C, etc. into three
  # elements: Whole String, Rank and Suit.
  def self.cards_from_hand_s(*hand_strings)
    number_of_hands = hand_strings.count
    hand_strings = hand_strings.map { |string| string = string.split }

    hand_size = hand_strings[0].count
    
    stacked_deck = []
    
    deck_array = []
    hand_size.downto(1) do |card_num| 
      hand_strings.count.times do |hand_num|
        deck_array << card_from_s(hand_strings[hand_num][card_num-1])
      end
    end
    deck_array.reverse
  end

  private
  # Returns an array of Playing Cards, based on a space separated string.
  CARD_REGEXP = /(10|[2-9]|[JQKA])\W*[of]*\W*([CHSD])/i
  def self.card_from_s(string)
    if rank_suit=CARD_REGEXP.match(string)
      Card.new(rank_suit[1], rank_suit[2])
    end
  end
end
