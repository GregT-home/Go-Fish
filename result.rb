class Result
  attr_reader :requester, :victim, :rank
  attr_accessor :matches, :received_from
  attr_accessor :books_made, :game_over

  def initialize(requester, victim, rank)
    @requester = requester
    @victim = victim
    @rank = rank

    @matches = 0
    @received_from = nil

    @books_made = 0
    @game_over = false
  end

  # part 1 : Player X asked for Ys from Player Z
  # part 2a: [got # matches] | [was told to 'Go Fish']
  # part 2b: (if deck) fished in pond [and got] | [did not get] a Y
  # part 3 :Player X [made a book] | [did not make a book]
  # part 4 : [the game is over] | [""]
  def to_s
    part1 = "Player ##{requester} asked for #{rank}s from player ##{victim}."

    if received_from == victim
      part2 = "Player got #{matches}."
    else
      part2 = "Player was told to 'Go Fish' and "
      if matches == 0
        part2 += "he did not get what he asked for from the pond."
      else
        part2 += "he got one from the pond!"
      end
    end
    
    if books_made == 0
      part3 = "He did not make a book."
    else
      part3 = "He made a book of #{rank}s."
    end

    if game_over
      part4 = "\nThe Game is now over"
    else
      part4 = ""
    end

   part1 + "\n" + part2 + "\n" + part3 + part4
  end

end # Result
