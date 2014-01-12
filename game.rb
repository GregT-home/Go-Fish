#
# Future features possibilities:
# 1) Currently, the game allows the player to lie about what is in his
# hand.  It might be an interesting feature to allow this, but allow
# other players to accuse him/her of lying, with an appropriate
# penalty, losing all books or losing the game, if rightly accused or
# the accuser getting the penalty if incorrect.
#
# 2) Alternately, prevent the player from asking for cards he does not
# possess.
#
# 3) Save a list of all moves made; potentially deck & game status as well (for roll-back or re-play)
# -Greg Jan 2014

require "./card.rb"
require "./deck.rb"
require "./hand.rb"
require "./result.rb"
class Game
  attr_reader :hands, :books_list, :deck, :current_hand, :current_index

  def initialize(num_hands, test_deck = [])
    @hands = []
    @books_list = {}
    @game_over = false
    @deck = Deck.new(test_deck)

    deck.shuffle if test_deck.empty?

    num_hands.times { |i|
      @hands << Hand.new()
      @books_list[@hands.last] = []
    }

    @current_index = 0
    @current_hand = hands[@current_index]
    deal(hand_size(num_hands), hands)
  end

  def hand_size(number_of_hands)
    if number_of_hands > 4
      5
    else
      7
    end
  end

  def books(hand)
    books_list[hand]
  end

  def advance_to_next_hand
    @current_index = (current_index + 1) % hands.length
    @current_hand = hands[@current_index]
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
      books_list[current_hand] << target_rank
      return 1
    else
      current_hand.receive_cards(cards)
      return 0
    end
  end

  def play_round(target_index, target_rank)
    victim_matches = hands[target_index].rank_count(target_rank)

    result = Result.new(current_hand, target_index, target_rank)

    if victim_matches > 0  # intended match
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
        if card.rank == target_rank  # intended match
          result.matches = 1
        else # possible surprise match
          if process_books(card.rank) == 1
            result.books_made += 1
            result.surprise_rank = card.rank
          end
          advance_to_next_hand  # no intended match anywhere: turn over
        end
      end
    end
    result.books_made += process_books(target_rank)
    result
  end
  def debug
    @debug = !@debug
  end

  def books_to_s(hand)
    books_list[hand].map { |i| i + "s"}.sort.join(", ")
  end

  def over?
    @game_over
  end
end # Game
