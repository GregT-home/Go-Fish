class Game
  attr_reader :hands, :deck, :current_hand

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

  # def process_books(target_rank)
  #   cards = @hands[@current_hand].give_matching_cards(target_rank)

  #   if cards.length == 4
  #     result.number_of_books_made = 1
  #   else
  #     @hands[@current_hand].receive_cards(cards)
  #   end
  # end    


  # returns nil if request failed.
  # returns result block with # of cards received
  def ask_hand_for_card(target_hand, target_rank)
    match_cards = target_hand.give_matching_cards(target_rank)

    result = Result.new(hands[@current_hand], target_hand, target_rank)

    if match_cards.length > 0
      hands[@current_hand].receive_cards(match_cards)
      result.number_of_cards_received += match_cards.length
      result.cards_received_from = target_hand
    end
    result
  end

  def play_round(target_hand, target_rank)
    result = ask_hand_for_card(target_hand, target_rank)

    # if we got cards from the target, then check for a book
    
    if result.number_of_cards_received > 0
      cards = @hands[@current_hand].give_matching_cards(target_rank)
      if cards.length == 4
        result.number_of_books_made = 1
      else
        @hands[@current_hand].receive_cards(cards)
      end
    end

    # if !result.number_of_cards.nil? we got what we asked for, then
    # the current hand has the cards and the target hand has had them
    # removed.
    if result.number_of_cards_received == 0
      card = @deck.give_card
      # no cards, game is over
      if card.nil?
        result.game_over=true
      else
        # cards: take the top one note that it is from the deck
        target_hand.receive_cards(card)
        result.number_of_cards_received = 1
        result.cards_received_from = :deck

        cards = @hands[@current_hand].give_matching_cards(target_rank)
        if cards.length == 4
          result.number_of_books_made = 1
        else
          @hands[@current_hand].receive_cards(cards)
        end
      end
    end
    result
  end


end # Game
