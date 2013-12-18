class FishHand
  attr_reader :cards

  def initialize(cards=[])
    @cards = cards
  end

  def give_card
    card = @cards.pop
  end

  def length
    @cards.length
  end

  def receive_card(newcard)
    @cards.unshift(newcard)  
  end

  def got_rank?(target_rank)
    @cards.select { |card| card.rank == target_rank } != []
  end

  def give_matching_ranked_cards(rank)
    @cards.select!{ |card| card.rank == rank }
  end

  def got_book?(rank)
        # search for a book
    # if found, delete & return book rank (i.e. if a book of 6s, then 6)
    # else return nil
    false
  end

  def remove_cards(these_cards)
    @cards - these_cards
  end

  def give_matching_cards(rank)
    return nil if get_cards_of_rank(rank) != []
  end

  private 
  def get_cards_of_rank(rank)
            cards.select { |card| card.rank == rank}
          end
 
end # FishHand

