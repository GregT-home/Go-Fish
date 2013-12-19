class Game
  attr_reader :hands, :current_hand

  def initialize(num_hands,test_deck = [])
    @hands = []
    @deck = Deck.new(test_deck)

    num_hands.times { |i|
      @hands[i] = Hand.new()
    }

    @current_hand = 0

    deal(num_hands, @hands)
  end

  def advance_to_next_hand
    @current_hand += 1
    @current_hand = @current_hand % hands.length
  end

  def deal(number, hands)
    number = @cards.length if number == 0
    number.times {
      hands.map { |hand|
        hand.receive_cards(@deck.give_card)
        }
    }
  end

  def play_round(requesting_hand, target_hand, target_rank)
    result = Result.new(requesting_hand, target_hand, target_rank)

    if target_hand.got_rank?(target_rank)
      cards = target_hand.give_matching_cards(target_rank)
      
      result.number_of_cards_received += cards.length
    else
      cards = @deck.give_card
      result.number_of_cards_received += 1
    end
      

  end

end # Game
