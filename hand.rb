class Hand
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

  def receive_cards(newcards)
    @cards.unshift(newcards)
    @cards.flatten!
  end

  def rank_count(target_rank)
    @cards.select { |card| card.rank == target_rank }.length
  end

  def give_matching_cards(rank)
    cards = @cards.select { |card| card.rank == rank }
    remove_cards(cards)
  end

  def got_book?(rank)
    cards = @cards.select { |card| card.rank == rank }
    cards.length == 4
  end

  def to_s
    cards.map {|card| "[" + card.to_s + "]"}.join (" ")
  end

  private 
  def get_cards_of_rank(rank)
            cards.select { |card| card.rank == rank}
          end

  def remove_cards(these_cards)
    @cards -= these_cards
    these_cards
  end
end # Hand
