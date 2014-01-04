require "./game.rb"
require "./player.rb"
require 'socket'

class FishServer
  # rspec reports these as being re-defined; unless clause inhibits this.
  PORT = 54011        unless const_defined?(:PORT)
  EOM_TOKEN = ":EOM:" unless const_defined?(:EOM_TOKEN)

  attr_reader :client_fd, :names, :players, :number_of_players, :game

  def initialize(number, test_deck = [])
    @client_fd = []
    @players = []
    @number_of_players = number
    @game = nil

    @game = Game.new(number_of_players, test_deck)
    @server = TCPServer.open(PORT)	# listen on our port
    STDOUT.puts "Listening for connections on %{PORT}" if @debug
  end

  def setup()
    get_clients
    create_players
    broadcast("The game begins...\n")

    # check hands for initial books
    players.each_with_index { |player, i|
      player.hand.cards.map { |card|
        if @game.process_books(card.rank) != 0
          broadcast "#{player.name} was dealt a book of #{card.rank}s.\n"
          break
        end
      }
    }
  end

  def game_play
    until @game.over? do
      player = players[@game.current_hand_index]
      broadcast("It is Player #{@game.current_hand_index}, #{player.name}'s turn.  ")
      put_message(player.fd, "Your cards: #{player.hand.to_s}\n")
      STDOUT.puts "debug: Deck has #{@game.deck.length} cards in it" if @debug
      loop { # loop for local commands
        put_message(player.fd, "What action do you want to take? ")
        raw_input = get_line(player.fd)
        args = raw_input.split
        if args[0] == "deck" && args[1] == "size"
          put_message(player.fd, "#{@game.deck.length} cards are left in the pond\n")
          next
        end
        if args[0] == "hand"
          put_message(player.fd, "Your cards: #{player.hand.to_s}\n")
          next
        end
        if args[0] == "ask"
          victim, rank = parse_ask(raw_input)
          puts victim.inspect, rank.inspect
          if victim || rank
            result = @game.play_round(victim, rank)
            broadcast(result.to_s)

            put_message(players[victim].fd,
                        "Your cards: #{players[victim].hand.to_s}\n")
            put_message(player.fd,
                        "Your cards: #{player.hand.to_s}\n")
            break
          end
        end # if ask
        put_message(player.fd,
                    "Not understood.  Choices are:\n[ask] <player> for <rank>\ndeck size\nhand\n")
      } # utility commmand loop
    end # game command loop
  end # game_play

  def  parse_ask(string)
    puts "parse_ask(#{string})"
    match = string.match(%r{\S*(10*|\d+).*(10|[2-9]|[JQKA])}i)
    puts match.inspect
    player_num = match[1].to_i
    rank = match[2]
    puts "match = #{match}, player_num = #{player_num}, rank = #{rank}"
    puts "returning #{player_num} and #{rank}"
    return player_num, rank
  end

  def run()
    setup
    broadcast("Play begins...\n")

    game_play

    endgame
  end

  def get_clients
    while client_fd.length < number_of_players
      client_fd << @server.accept 
      #consume the "new player" response and let the client know
      STDOUT.puts "get_clients: accepting a new client" if @debug
      client_fd[-1].puts get_line(client_fd[-1])
    end
  end

  # get name, associate
  def create_players
    i = 0
    while i < number_of_players do
      begin
        put_message(client_fd[i], "what is your name? ")
        name = get_line(client_fd[i]).strip
      end while name.empty?
      players << Player.new(name, @game.current_hand, client_fd[i])
# gt Jan-2014. causes put_message test in server.spec to fail, need to
# investigate why
#      put_message(players[-1].fd, @game.current_hand.to_s)
      @game.advance_to_next_hand
      i += 1
    end
  end

def endgame
    broadcast "There are no more fish in the pond.  Game play is over.\n"
    broadcast "Here is the final outcome:\n"

    rank_list = calculate_rankings

    winner_count = 0
    rank_list.each { |rank| winner_count += 1 if rank == 0 }

    players.each_with_index { |player, i|
      part1 = "Player #{i}, #{player.name} made " +
                 "#{@game.books[i].length} books (#{@game.books_to_s(i)})"

      if rank_list[i] == 0
        broadcast part1 + " and is the winner!\n" if winner_count == 1
        broadcast part1 + " and ties for the win!\n" if winner_count > 1
      end
    }
  end

  def calculate_rankings
    book_count = []
    players.each_with_index { |player, i| book_count << @game.books[i].length }

    # 1: make a list of the ranks we have
    # 2: review the book_count list to see who has what ranking
    # Final result now indicates player rankings. Duplicates indicate ties.
    list = book_count.sort.uniq.reverse
    book_count.map { |bucket| list.index(bucket) }
  end

  def put_message(fd, msg)
    fd.puts msg + EOM_TOKEN
    STDOUT.puts("Debug: (to #{fd.inspect})" + msg) if @debug
  end

  def broadcast(msg)
    @client_fd.map { |cli|
      put_message(cli, msg)
    }
  end

  def close
    @server.close
    @client_fd.each { |fd| fd.close }
    @client_fd.clear
  end

  def debug
    @debug = !@debug
  end

private
  def get_line(fd)
    begin
      input = fd.gets.chomp
      STDOUT.puts "Debug: (input from #{fd.inspect}" + input if @debug

    rescue => reason
      STDOUT.puts "Debug: player lost: #{reason.to_s}" if @debug
    end
    input
  end

  # def put_line(fd, line)
  #   fd.puts line
  # end

end # Fish_Server
