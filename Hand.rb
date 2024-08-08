class Hand
  attr_reader :cards

  def initialize(cards=nil)
    @cards = cards ? @cards = cards : @cards = []
  end

  def give_card
    card = @cards.pop
  end

  def count
    @cards.count
  end

  def receive_cards(newcards)
    @cards.unshift(newcards)
    @cards.flatten!
    sort!
  end

  def sort!
    @cards.sort! { |c1, c2| c2.rank <=> c1.rank }
  end

  def rank_count(target_rank)
    @cards.select { |card| card.rank == target_rank }.count
  end

  def give_matching_cards(rank)
    cards = @cards.select { |card| card.rank == rank }
    remove_cards(cards)
  end

  def got_book?(rank)
#    cards = @cards.select { |card| card.rank == rank }
#    cards.count == 4
    rank_count(rank) == 4
  end

  def to_s
    cards.map {|card| "[" + card.to_s + "]"}.join(" ")
  end

  private 

  def remove_cards(these_cards)
    @cards -= these_cards
    these_cards
  end
end # Hand
