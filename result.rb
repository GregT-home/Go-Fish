class Result
  attr_reader :requester, :victim, :rank
  attr_accessor :number_received, :received_from
  attr_accessor :number_of_books_made, :game_over

  def initialize(requester, victim, rank)
    @requester = requester
    @victim = victim
    @rank = rank

    @number_received = 0
    @received_from = nil

    @number_of_books_made = 0
    @game_over = false
  end

# Player X asked for Ys from Player Z
# [and got #] | [but was told to 'Go Fish']
# (if deck) Player X fished in the pond [and got] | [did not get] a Y
# Player X [made a book] | [did not make a book]
# [the game is over] | [""]
def to_s
  part1 = "Player ##{requester} asked for #{rank}s from player ##{victim}"
  if received_from != victim
    part2 = " and was told to 'Go Fish.'"
  else
    part2 = " and got #{number_received}."
  end
  
  if number_of_books_made > 0
    part3 = "He made a book of #{rank}s."
  else
    part3 = "He did not make a book."
  end

  if game_over
    part4 = "\nThe Game is now over"
  else
    part4 = ""
end

  part1 + part2 + "\n" + part3 + part4
end

end # Result
