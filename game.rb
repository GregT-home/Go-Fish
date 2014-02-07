# To do:
# merge concept of hands and players.  A player should have a hand,
# the game should run from players.

require "./card.rb"
require "./deck.rb"
require "./hand.rb"
require "./result.rb"
require "./player.rb"
require "pry"

class Game
  GAME_OVER_TOKEN = "::GAME_OVER::" unless const_defined?(:GAME_OVER_TOKEN)

  private
  attr_reader :current_player_index

  public
  attr_reader :books_list, :pond, :players

  def initialize()
    @players = []
    @books_list = {}
    @game_over = false
    @current_player_index = 0
    @game_is_started = false
  end

  def start_game(cards = nil)
    return nil if @game_is_started 
    if cards.nil?
      @pond = Deck.new()
    else
      @pond = Deck.new(cards)
    end

    @players.each {  |player| @books_list[player] = [] }
    @current_player_index = 0
    deal(@players.count > 4 ? 5: 7)
    @game_is_started = true
  end

  def started
    @game_is_started
  end

  def deal(number)
    number.times do
      @players.each { |player| player.hand.receive_cards(@pond.give_card) }
    end
  end

  def pond_size
      @pond.count
  end

  def add_player(number, name)
    unless @game_is_started
      hand = Hand.new()
      player = Player.new(number, name, hand)
      players << player
      player.tell("Waiting for the rest of the players.")
      advance_to_next_player unless @players.empty?
    end
  end

  def current_player
    @players[@current_player_index]
  end

  def player_from_number(number)
    hit = players.detect() { |player| player.number == number}
    return hit.nil? ? nil : hit
  end    

  def number_of_players
    @players.count
  end

  def advance_to_next_player
    @current_player_index = (current_player_index + 1) % @players.count
  end

  def books(player)
    books_list[player]
  end

  def books_to_s(player)
    if books(player).nil? || books(player).empty?
      ""
    else
      books(player).map { |rank| rank + "s"}.sort.join(", ")
    end
  end

  def number_of_books(player)
    if books(player).nil? || books(player).empty?
      0
      else
      books(player).count
    end    
  end

  # check for book, if found then remove and return true, else false.
  def process_books(target_rank)
    cards = current_player.hand.give_matching_cards(target_rank)
    if cards.count == 4
      books_list[current_player] << target_rank
      return true
    else
      current_player.hand.receive_cards(cards)
      return false
    end
  end

  def play_round(target_player, target_rank)
#    puts "-", "play_round: #{current_player.name} asking #{target_player.name} for #{target_rank}"
#    puts "current hand: #{current_player.hand}"
#    puts "target hand: #{target_player.hand}"
    result = Result.new(current_player, target_player, target_rank)

    if target_player.hand.rank_count(target_rank) > 0  # has the rank
#puts "-", "target player has the rank"
      match_cards = target_player.hand.give_matching_cards(target_rank)
      current_player.hand.receive_cards(match_cards)

      result.matches += match_cards.count
      result.received_from_player = true
#puts "-", result
    else 
      card = pond.give_card
      if card.nil?     # no cards, game is over
        @game_over = result.game_over = true
      else
#        puts "-", "got a card from the pond"
        current_player.hand.receive_cards(card)
        result.received_from_pond = true
        if card.rank == target_rank  # intended match
#          puts "-", "it is what player asked for"
          result.matches = 1
        else # possible surprise match
#          puts "-", "it is NOT what player asked for"
          if process_books(card.rank)
#          puts "-", "BUT, he made a surprise book of #{card.rank}"
            result.book_made = true
            result.surprise_rank = card.rank
          end
#          puts "-", result
          advance_to_next_player  # no intended match anywhere: turn over
        end
      end
    end
    result.book_made = process_books(target_rank) if result.book_made == nil;
    result
  end

  def debug
    @debug = !@debug
  end

  def over?
    @game_over
  end

#
# methods below this point really belong to the controller and not the
# game.  Not sure what the object should be.
#


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
      player = @game.current_player
      broadcast("-------------------\n" +
                "It is Player #{player.number}, #{player.name}'s turn.\n")
      player.tell("Your cards: #{player.hand.to_s}\n")

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
    @players.each_with_index do |player, i|
      part1 = "Player #{player.number}, #{player.name}, made " +
        "#{books(player).count} books (#{books_to_s(player)})"

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

    if (args[0] == "deck" && args[1] == "size") ||
       (args[0] == "pond" && args[1] == "size")
      player.tell( "#{pond_size} cards are left in the pond\n")
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
                "    pond size\n" +
                "    hand\n" + 
                "    status\n")
    return :private
  end

  def give_player_status(to_player)
    players.each do |player|
      to_player.tell ("  #{player.name} (##{player.number})"+
                   " has #{player.hand.count}" +
                   " cards and has made #{number_of_books(player)} books" +
                   " (#{books_to_s(player)})\n")
    end
    to_player.tell("  Pond has #{pond_size} cards remaining.\n")
  end


  def process_ask(raw_input, player)
    victim_number, rank = parse_ask(raw_input)

    if !victim_number
      player.tell("Victim and/or rank not recognized.\n")
      return false
    end

    victim = player_from_number(victim_number)

    if victim.nil?
      player.tell("That player does not exist.\n")
      return false
    end

    if victim == player
      player.tell("?? You cannot request cards from yourself.\n")
      return false
    end

    result = play_round(victim, rank)
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
    players.each { |player| player_books << books(player).count }

    # 2: make a list of the rankings we have
    # 3: review the player_books list to see who has what ranking
    # Final result now indicates player rankings. Duplicates indicate ties.
    bucket_list = player_books.sort.uniq.reverse
    player_books.map { |player| bucket_list.index(player) }
  end

  def tell_all(message)
    players.each { |player| player.tell(message) }
  end

  # def tell_all_but_this_owner(players, omit_player, message)
  #   players.each do |player|
  #     player.tell(message) unless player == omit_player
  #   end
  # end

end # Game
