require "./game.rb"
require "./player.rb"
require 'socket'

class FishServer
  # rspec reports these as being re-defined; unless clause inhibits this.
  PORT = 54011        unless const_defined?(:PORT)
  EOM_TOKEN = ":EOM:" unless const_defined?(:EOM_TOKEN)
  GAME_OVER_TOKEN = "::GAME_OVER::" unless const_defined?(:GAME_OVER_TOKEN)
  Help_string =<<-EOF
  Choices are:
    ask <player #> for <rank>
    deck size
    hand
    status
EOF

  attr_reader :client, :names, :players, :number_of_players, :game

  def initialize(number, test_deck = [])
    @client = []
    @players = []
    @number_of_players = number
    @game = nil

    @game = Game.new(number_of_players, test_deck)
    @server = TCPServer.open(PORT)	# listen on our port
    log "Listening for connections on %{PORT}"
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
      player = players.select { |player| player.hand == @game.current_hand }[0]
      broadcast("-------------------\n" +
                "It is Player #{player.number}, #{player.name}'s turn.\n")
      put_message(player.socket, "Your cards: #{player.hand.to_s}\n")
      log "Deck has #{@game.deck.length} cards in it"

      loop do
        put_message(player.socket, "What action do you want to take? ")
        raw_input = get_line(player.socket)

        if process_commands(player, raw_input) == :private
          next  # no status update needed
        else
          break # broadcast status update
        end
      end
    end
  end # game_play

  def endgame
    broadcast ("=========================\n" +
               "There are no more fish in the pond.  Game play is over.\n" +
               "Here is the final outcome:\n")

    rank_list = calculate_rankings
    winners = 0
    rank_list.each { |rank| winners += 1 if rank == 0 }

    players.each do |player|
      part1 = "Player #{player.number}, #{player.name}, made " +
        "#{@game.books(player.hand).length} books (#{@game.books_to_s(player.hand)})"

      # rank_list is one-off from player numbers
      if rank_list[player.number - 1] == 0
        broadcast part1 + " and is the winner!\n" if winners == 1
        broadcast part1 + " and ties for the win!\n" if winners > 1
      else
        broadcast part1 + "\n"
      end
    end
    broadcast ("Thank you for Playing.\n" +
               "=========================\n")
    broadcast GAME_OVER_TOKEN
  end

  def put_status(socket)
    players.each do |player|
      put_message(socket,
                  "  #{player.name} (##{player.number}) has #{player.hand.length}" +
                  " cards and has made #{@game.books(player.hand).length} books" +
                  " (#{@game.books_to_s(player.hand)})\n")
    end
    put_message(socket, "  Deck has #{@game.deck.length} cards remaining.\n")
  end

  def process_commands(player, raw_input)
    args = raw_input.split

    if args[0] == "deck" && args[1] == "size"
      put_message(player.socket,
                  "#{@game.deck.length} cards are left in the pond\n")
      return :private # utility command
    end

    if args[0] == "hand" || args[0] == "cards"
      put_message(player.socket, "Your cards: #{player.hand.to_s}\n")
      return :private # utility command
    end

    if args[0] == "status"
      put_status(player.socket)
      return :private # utility command
    end

    if args[0] == "ask"
      if process_ask(raw_input, player)
        return :public # game
      end
      return :private
    end
    put_message(player.socket, "Not understood.\n" + Help_string)
    return :private
  end

  def process_ask(raw_input, player)
    victim_number, rank = parse_ask(raw_input)

    if !victim_number
      put_message(player.socket, "Victim and/or rank not recognized.\n")
      return false
    end

    victim = players.select { |player| player.number == victim_number}[0]

    if victim.nil?
      put_message(player.socket, "That player does not exist.\n")
      return false
    end

    if victim == player
      put_message(player.socket, "?? You cannot request cards from yourself.\n")
      return false
    end

    victim_index = victim.number - 1

    result = @game.play_round(victim_index, rank)
    broadcast("#{player.name} (player ##{player.number})," +
              " asked for #{rank}s from player" +
              " ##{victim.number}, #{victim.name}.\n" +
              result.to_s)
    put_message(victim.socket, "Your cards: #{victim.hand.to_s}\n")
    put_message(player.socket, "Your cards: #{player.hand.to_s}\n")
    true
  end

  def  parse_ask(string)
    log "parse_ask(#{string})"
    match = string.match(%r{\D*(\d+).*(10|[2-9]|[JQKA])}i)
    log "parse_ask: match = #{match}"
    log "parse_ask: #{match.inspect}"
    if match
      player_num = match[1].to_i unless match[1].nil?
      rank = match[2].upcase unless match[2].nil?
      log "parse_ask: returning #{player_num} and #{rank}"
    end
    return player_num, rank
  end

  def run()
    setup
    game_play
    endgame
  end

  def get_clients
    while client.length < number_of_players
      client << @server.accept 
      log "get_clients: accepting a new client"
      #consume the "new player" response and let the client know
      client.last.puts get_line(client.last)
    end
  end

  # get name, associate
  def create_players
    i = 0
    while i < number_of_players do
      begin
        put_message(client[i], "What is your name? ")
        name = get_line(client[i]).strip
      end while name.empty?
      players << Player.new(i+1, name, @game.current_hand, client[i])
      put_message(players.last.socket,
                  "Your cards: #{players[-1].hand.to_s}\n")
      @game.advance_to_next_hand
      i += 1
    end
  end


  def calculate_rankings
    # 1. make an array of the number of books each player made
    player_books = []
    players.each { |player| player_books << @game.books(player.hand).length }

    # 2: make a list of the rankings we have
    # 3: review the player_books list to see who has what ranking
    # Final result now indicates player rankings. Duplicates indicate ties.
    bucket_list = player_books.sort.uniq.reverse
    player_books.map { |player| bucket_list.index(player) }
   end

  def put_message(socket, msg)
    socket.puts "  "+ msg + EOM_TOKEN
    log "(to #{socket.inspect})" + msg
  end

  def broadcast(msg)
    @client.map { |cli| put_message(cli, msg) }
  end

  def close
    @server.close
    @client.each { |fd| fd.close }
    @client.clear
  end

  def debug
    @debug = !@debug
  end

private
  def get_line(socket)
    begin
      input = socket.gets.chomp
      log "(input from #{socket.inspect}" + input

    rescue => reason
      log "player lost: #{reason.to_s}"
    end
    input
  end

  def log(message)
    STDOUT.puts "Log: " + message if @debug
  end
end # Fish_Server
