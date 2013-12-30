class Result
  attr_reader :requesting_hand, :target_hand, :target_rank
  attr_accessor :number_of_cards_received, :cards_received_from
  attr_accessor :number_of_books_made, :game_over

  def initialize(requesting_hand, target_hand, target_rank)
    @requesting_hand = requesting_hand
    @target_hand = target_hand
    @target_rank = target_rank

    @number_of_cards_received = 0
    @cards_received_from = nil

    @number_of_books_made = 0
    @game_over = false
  end

# Player X asked for Ys from Player Z
# [and got #] | [but was told to 'Go Fish']
# (if deck) Player X fished in the pond [and got] | [did not get] a Y
# Player X [made a book] | [did not make a book]
# [the game is over] | [""]
def to_s
  part1 = "Player #{@requesting_hand} asked for #{@target_rank}s from player #{@target_hand}"
  if @cards_received_from != @target_hand
    part2 = " and was told to 'Go Fish.'"
  else
    part2 = "and got #{@number_of_cards_received}."
  end
  
  if @number_of_books_made > 0
    part3 = "He made a book of #{@target_rank}s."
  else
    part3 = "He did not make a book."
  end

  if @game_over
    part4 = "\nThe Game is now over"
  else
    part4 = ""
end

  part1 + part2 + "\n" + part3 + part4
end

end # Result
