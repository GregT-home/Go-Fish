require "./card.rb"
require "./deck.rb"
require "./hand.rb"
require "./result.rb"
require "./player.rb"
require "pry"


class Game
  GAME_OVER_TOKEN = "::GAME_OVER::" unless const_defined?(:GAME_OVER_TOKEN)

  private
  attr_reader :current_hand_index

  public
  attr_reader :hands, :books_list, :deck, :current_hand, :players

  def initialize()
    @hands = []
    @players = {}
    @books_list = {}
    @ready_to_start = false
    @game_over = false
    @current_hand_index = 0
  end

  def start_game(cards = nil)
    if cards.nil?
      @deck = Deck.new()
    else
      @deck = Deck.new(cards)
    end

    @hands.each {  |hand| @books_list[hand] = [] }
    @current_hand = @hands.first
    deal(@hands.count > 4 ? 5: 7)
  end

  def add_hand
      @hands << Hand.new()
  end

  def add_player(player)
    if @ready_to_play
      return nil
    else
      @players[@hands[@current_hand_index]] = player
      advance_to_next_hand
      @ready_to_play = true if current_hand_index == 0
      player
    end    
  end

  def owner(hand)
    @players[hand]
  end

  def hand_from_player_number(number)
    players.select { |hand, player| player.number == number}.keys[0]
  end

  def number_of_hands
    @hands.count
  end

  def books(hand)
    books_list[hand]
  end

  def advance_to_next_hand
    @current_hand_index = (current_hand_index + 1) % @hands.count
    @current_hand = @hands[@current_hand_index]
  end

  def deal(number)
    number.times do
      @hands.each { |hand| hand.receive_cards(@deck.give_card) }
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

  def setup()
    get_clients
    create_players
    broadcast("=====================\nAnd now play begins...\n")
    check_players_for_books
  end

  def check_players_for_books
    players.each do |player|
      player.hand.cards.map do |card|
        if @game.process_books(card.rank) != 0
          broadcast "#{player.name} was dealt a book of #{card.rank}s.\n"
          break
        end
      end
    end
  end

  def game_play
    until @game.over? do
#      player = players.select { |player| player.hand == @game.current_hand }[0]
      player = @game.owner(@game.current_hand)
      broadcast("-------------------\n" +
                "It is Player #{player.number}, #{player.name}'s turn.\n")
      player.tell("Your cards: #{player.hand.to_s}\n")
#      log "Deck has #{@game.deck.count} cards in it"

      loop do
        player.tell("What action do you want to take? ")
        raw_input = player.ask

        if process_commands(player, raw_input) == :private
          next  # no status update needed
        else
          break # broadcast status update
        end
      end
    end
  end # game_play

  def endgame
    tell_all ("=========================\n" +
               "There are no more fish in the pond.  Game play is over.\n" +
               "Here is the final outcome:\n")

    rank_list = calculate_rankings
    winners = 0
    rank_list.each { |rank| winners += 1 if rank == 0 }
    @hands.each_with_index do |hand, i|
      part1 = "Player #{owner(hand).number}, #{owner(hand).name}, made " +
        "#{books_list[hand].count} books (#{books_to_s(hand)})"

      # rank_list is one-off from hand numbers
      if rank_list[i] == 0
        tell_all part1 + " and is the winner!\n" if winners == 1
        tell_all part1 + " and ties for the win!\n" if winners > 1
      else
        tell_all part1 + "\n"
      end
    end
    tell_all ("Thank you for Playing.\n" +
               "=========================\n")
    tell_all GAME_OVER_TOKEN
  end

  def process_commands(player, raw_input)
    args = raw_input.split

    if args[0] == "deck" && args[1] == "size"
      player.tell( "#{deck.count} cards are left in the pond\n")
      return :private # utility command
    end

    if args[0] == "hand" || args[0] == "cards"
      player.tell("Your cards: #{player.hand.to_s}\n")
      return :private # utility command
    end

    if args[0] == "status"
      give_player_status(player)
      return :private # utility command
    end

    if args[0] == "ask"
      if process_ask(raw_input, player)
        return :public # game
      end
      return :private
    end

    player.tell("Not understood.\n" +
                "  Choices are:\n" +
                "    ask <player #> for <rank>\n" +
                "    deck size\n" +
                "    hand\n" + 
                "    status\n")
    return :private
  end

  def give_player_status(player)
    hands.each do |hand|
      player.tell ("  #{owner(hand).name} (##{owner(hand).number})"+
                   " has #{hand.count}" +
                   " cards and has made #{books_list[hand].count} books" +
                   " (#{books_to_s(hand)})\n")
    end
    player.tell("  Deck has #{deck.count} cards remaining.\n")
  end


  def process_ask(raw_input, player)
    victim_number, rank = parse_ask(raw_input)

    if !victim_number
      player.tell("Victim and/or rank not recognized.\n")
      return false
    end

    victim_hand = hand_from_player_number(victim_number)
    victim = owner(victim_hand)

    if victim.nil?
      player.tell("That player does not exist.\n")
      return false
    end

    if victim == player
      player.tell("?? You cannot request cards from yourself.\n")
      return false
    end

    result = play_round(victim_hand, rank)
    tell_all("#{player.name} (player ##{player.number})," +
              " asked for #{rank}s from player" +
              " ##{victim.number}, #{victim.name}.\n" +
              result.to_s)
    victim.tell "Your cards: #{victim.hand.to_s}\n"
    player.tell "Your cards: #{player.hand.to_s}\n"
    true
  end

  def  parse_ask(string)
#    log "parse_ask(#{string})"
    match = string.match(%r{\D*(\d+).*(10|[2-9]|[JQKA])}i)
#    log "parse_ask: match = #{match}"
#    log "parse_ask: #{match.inspect}"
    if match
      player_num = match[1].to_i unless match[1].nil?
      rank = match[2].upcase unless match[2].nil?
#      log "parse_ask: returning #{player_num} and #{rank}"
    end
    return player_num, rank
  end

  def calculate_rankings
    # 1. make an array of the number of books each player made
    player_books = []
#    players.each { |player| player_books << @game.books(player.hand).count }
    hands.each { |hand| player_books << books_list[hand].count }

    # 2: make a list of the rankings we have
    # 3: review the player_books list to see who has what ranking
    # Final result now indicates player rankings. Duplicates indicate ties.
    bucket_list = player_books.sort.uniq.reverse
    player_books.map { |player| bucket_list.index(player) }
  end

  def tell_owner(hand, message)
    owner(hand).tell(message)
  end

  def tell_all(message)
    hands.each { |hand| tell_owner(hand, message) }
  end

  def tell_all_but_this_owner(hands, omit_hand, message)
    hands.each do |hand|
      tell_owner(hand, message) unless hand == omit_hand
    end
  end


  # def run()
  #   setup
  #   game_play
  #   endgame
  # end

end # Game
