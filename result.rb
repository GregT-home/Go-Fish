class Result
  attr_reader :requesting_hand, :target_hand, :target_rank
  attr_accessor :number_of_cards_received, :number_of_books_made

  def initialize(requesting_hand, target_hand, target_rank)
    @requesting_hand = requesting_hand
    @target_hand = target_hand
    @target_rank = target_rank
  end


end # Result
