require "./card.rb"
require "./deck.rb"
require "./hand.rb"
require "./result.rb"
class Game
  attr_reader :hands, :books, :deck, :current_hand_index, :current_hand

  def initialize(num_hands, test_deck = [])
    @hands, @books = [], []
    @game_over = false
    @deck = Deck.new(test_deck)

    deck.shuffle if test_deck.empty?

    num_hands.times { |i|
      @hands[i] = Hand.new()
      books[i] = []
    }

    @current_hand_index = 0
    @current_hand = hands[current_hand_index]

    deal((num_hands > 4) ? 5 : 7, hands)
  end

  def advance_to_next_hand
    @current_hand_index = (current_hand_index + 1) % hands.length
    @current_hand = hands[current_hand_index]
  end

  def deal(number, hands)
    number = cards.length if number == 0
    number.times {
      hands.map { |hand|
        hand.receive_cards(deck.give_card)
        }
    }
  end

  # check for book, if found then remove and return 1, else 0.
  def process_books(target_rank)
    cards = current_hand.give_matching_cards(target_rank)
    if cards.length == 4
      books[current_hand_index] << target_rank
      return 1
    else
      current_hand.receive_cards(cards)
      return 0
    end
  end

  def play_round(target_index, target_rank)
    victim_matches = hands[target_index].rank_count(target_rank)

    result = Result.new(current_hand_index, target_index, target_rank)

    if victim_matches > 0
      match_cards = hands[target_index].give_matching_cards(target_rank)
      current_hand.receive_cards(match_cards)

      result.matches += match_cards.length
      result.received_from = target_index
    else
      card = deck.give_card
      if card.nil?     # no cards, game is over
        @game_over = result.game_over = true
      else
        current_hand.receive_cards(card)
        result.received_from = :pond
        if card.rank == target_rank
          result.matches = 1
        else
          advance_to_next_hand  # no matches anywhere: turn over
        end
      end
  end
    result.books_made = process_books(target_rank)
    result
  end

  def books_to_s(index)
    books[index].sort.join(", ")
  end

  def over?
    @game_over
  end
end # Game
