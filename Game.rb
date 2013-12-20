class Game
  attr_reader :hands, :current_hand

  def initialize(num_hands,test_deck = [])
    @hands = []
    @deck = Deck.new(test_deck)

    num_hands.times { |i|
      @hands[i] = Hand.new()
    }

    @current_hand = 0

    deal(6, @hands)
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

  def ask_hand_for_card(requesting_hand, target_hand, target_rank)
    number_received = target_hand.give_matching_cards(target_rank).length

    result = Result.new(requesting_hand, target_hand, target_rank)

    if number_received > 0
      result.number_of_cards_received += number_received
      result.cards_received_from = target_hand
    # else
    #   result.cards_received_from = nil
    end
    result
  end

  # Hand X asks Hand Y for card Z
  # if he gets it: done; player gets another turn
  # if he does not get it, then "go fish" from the deck
  #   if he gets his choice from the deck: done; player gets another turn
  #   if he does not, then player's turn is complete
  # Result will reflect:
  #  cards received
  #  source of cards (player or deck)
  def play_round(requesting_hand, target_hand, target_rank)
    result = ask_hand_for_card(requesting_hand, target_hand, target_rank)

    nil
#    if result.cards_received_from
      

    
  end


end # Game
