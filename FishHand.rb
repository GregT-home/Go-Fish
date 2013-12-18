class FishHand
  attr_reader :interactive,  :active_cards, :war_chest,  :name

  def initialize(active_cards=[])
    @active_cards = active_cards
  end

  def give_card
    card = @active_cards.pop
  end

  def length
    @active_cards.length
  end

  def receive_card(newcard)
    @active_cards.unshift(newcard)  
  end

  def got_rank?(rank)
    @cards.select { |card| card.rank = rank } != []
  end

  def give_matching_ranked_cards(rank)
    @cards.select!{ |card| card.rank = rank }
  end

  def got_book?(rank)
        # search for a book
    # if found, delete & return book rank (i.e. if a book of 6s, then 6)
    # else return nil
    false
  end

  def remove_cards(cards)
    @active_cards - cards
  end

  def give_matching_cards(rank)
    return nil if get_cards_of_rank(rank) != []
  end

  private 
  def get_cards_of_rank(rank)
            active_cards.select { |card| card.rank == rank}
          end
 
end # FishHand

