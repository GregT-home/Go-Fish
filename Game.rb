class Game
  attr_reader :hands, :deck, :current_hand_index, :current_hand

  def initialize(num_hands, test_deck = [])
    @hands = []
    @deck = Deck.new(test_deck)

    num_hands.times { |i|
      @hands[i] = Hand.new()
    }

    @current_hand_index = 0
    @current_hand = @hands[current_hand_index]

    deal((num_hands > 4) ? 5 : 7, @hands)
  end

  def advance_to_next_hand
    @current_hand_index += 1
    @current_hand_index = @current_hand_index % hands.length
    @current_hand = @hands[@current_hand_index]
  end

  def deal(number, hands)
    number = @cards.length if number == 0
    number.times {
      hands.map { |hand|
        hand.receive_cards(@deck.give_card)
        }
    }
  end

  # check for book, if found then remove and return 1, else 0.
  def process_books(target_rank)
    cards = @current_hand.give_matching_cards(target_rank)
    if cards.length == 4
      return 1
    else
      @current_hand.receive_cards(cards)
      return 0
    end
  end

  # returns nil if request failed.
  # returns result block with # of cards received
  # removes cards from target_hand and places into current hand
  def ask_for_matches(target_hand, target_rank)
    result = Result.new(@current_hand, target_hand, target_rank)

    match_cards = target_hand.give_matching_cards(target_rank)

    if match_cards.length > 0
      @current_hand.receive_cards(match_cards)
      result.number_of_cards_received += match_cards.length
      result.cards_received_from = target_hand
      result.number_of_books_made = process_books(target_rank)
    end
    result
  end

  def play_round(target_hand, target_rank)
    result = ask_for_matches(target_hand, target_rank)

    if result.number_of_cards_received == 0
      card = @deck.give_card
      #  puts "card = #{card.inspect}"
      # no cards, game is over
      if card.nil?
        result.game_over=true
      else
        # cards: take the top one note that it is from the deck
        target_hand.receive_cards(card)
        result.number_of_cards_received = 1
        result.cards_received_from = :deck
        @current_hand.give_matching_cards(target_rank)
      end
    end
    result
  end
end # Game
