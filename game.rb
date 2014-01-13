require "./card.rb"
require "./deck.rb"
require "./hand.rb"
require "./result.rb"
class Game
  private
  attr_reader :current_hand_index

  public
  attr_reader :hands, :books_list, :deck, :current_hand

  def initialize(num_hands, test_deck = [])
    @hands = []
    @books_list = {}
    @game_over = false
    @deck = Deck.new(test_deck)

    deck.shuffle if test_deck.empty?

    num_hands.times do |i|
      @hands << Hand.new()
      @books_list[@hands.last] = []
    end

    @current_hand = hands.first
    @current_hand_index = 0

    if num_hands > 4
      deal(5, hands)
    else
      deal(7, hands)
    end
  end

  def books(hand)
    books_list[hand]
  end

  def advance_to_next_hand
    @current_hand_index = (current_hand_index + 1) % hands.count
    @current_hand = hands[@current_hand_index]
  end

  def deal(number, hands)
    number = cards.count if number == 0
    number.times do
      hands.map { |hand| hand.receive_cards(deck.give_card) }
    end
  end

  # check for book, if found then remove and return 1, else 0.
  def process_books(target_rank)
    cards = current_hand.give_matching_cards(target_rank)
    if cards.count == 4
      books_list[current_hand] << target_rank
      return 1
    else
      current_hand.receive_cards(cards)
      return 0
    end
  end

  def play_round(target_hand, target_rank)
    victim_matches = target_hand.rank_count(target_rank)

    result = Result.new(current_hand, target_hand, target_rank)

    if victim_matches > 0  # intended match
      match_cards = target_hand.give_matching_cards(target_rank)
      current_hand.receive_cards(match_cards)

      result.matches += match_cards.count
      result.received_from = target_hand
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
