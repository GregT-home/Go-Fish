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

  def run()
    get_clients
    create_players
    broadcast("The begins.  Dealing cards...\n")
    @game.check_all_for_books { |result|
      if result.number_of_books_made > 0
        broadcast("#{@players[result.requester].name} was dealt " +
                  "a book of #{result.rank}s.\n")
      end
    }

    broadcast("Play begins...\n")

    until @game.over? do
      player = players[@game.current_hand_index]
      broadcast("It is #{player.name}'s turn.  ")
      put_message(player.fd, "Your cards are: #{player.hand.to_s}\n")
      # test: ask self for 2s
    STDOUT.puts "debug: Deck has #{@game.deck.length} cards in it"
      result = @game.play_round(0,"2")
      broadcast(result.to_s)
    end
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
      @game.advance_to_next_hand
      i += 1
    end
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
    input = fd.gets.chomp
    STDOUT.puts "Debug: (input from #{fd.inspect}" + input if @debug
    input
  end

  # def put_line(fd, line)
  #   fd.puts line
  # end

end # Fish_Server
