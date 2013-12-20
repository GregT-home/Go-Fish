class Result
  attr_reader :requesting_hand, :target_hand, :target_rank
  attr_accessor :number_of_cards_received, :cards_received_from, :number_of_books_made

  def initialize(requesting_hand, target_hand, target_rank)
    @requesting_hand = requesting_hand
    @target_hand = target_hand
    @target_rank = target_rank
    @number_of_cards_received = 0
    @cards_received_from = nil
    @number_of_books_made = 0
  end


end # Result
