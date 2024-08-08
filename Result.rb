class Result
  attr_reader :requester, :victim, :rank
  attr_accessor :matches, :received_from_player, :received_from_pond
  attr_accessor :book_made
  attr_accessor :surprise_rank, :game_over

  def initialize(requester, victim, rank)
    @requester = requester
    @victim = victim
    @rank = rank

    @matches = 0
    @received_from = nil

    @book_made = nil
    @surprise_rank = nil
    @game_over = false
  end

  # part 1a: [got # matches] | [was told to 'Go Fish']
  # part 1b: (if deck) fished in pond [and got] | [did not get] a Y
  # part 2 :Player X [made a book] | [did not make a book]
  # part 3 : [the game is over] | [""]
  def to_s
    part0 = ""
    if received_from_player
      part1 = "Player got #{matches}."
    else
      part1 = "Player was told to 'Go Fish' and "
      if matches == 0
        part1 += "he did not get what he asked for from the pond."
      else
        part1 += "he got one from the pond!"
      end
    end
    
    if ! book_made
      part2 = "He did not make a book."
    else
      if surprise_rank.nil?
        part2 = "He made a book of #{rank}s."
      else
        part2 = "He was surprised to make a book of #{surprise_rank}s."
      end
    end

    if game_over
      part3 = "\nThe Game is now over"
    else
      part3 = ""
    end

   part0 + part1 + "\n" + part2 + part3
  end
end # Result
