require 'socket'

class FishServer
  PORT = 54011
  EOM_TOKEN = ":EOM:"

  attr_reader :client_fd, :names, :players, :number_of_players, :game

  def initialize(number, test_deck = [])
    @client_fd = []
    @players = []
    @number_of_players = number
    @game = nil

    @game = Game.new(number_of_players, test_deck)
    @server = TCPServer.open(PORT)	# listen on our port
  end

  def run()
    get_clients
    create_players
    check_all_for_books
    @game.play_round until @game.over?
  end

  def get_clients
      while client_fd.length < number_of_players
        client_fd << @server.accept 
        #consume the "new player" response and let the client know
        put_line(client_fd[-1], get_line(client_fd[-1]))
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
      players << Player.new(@game.current_hand, name, client_fd[i])
      @game.advance_to_next_hand
      i += 1
    end
  end

  def put_line(fd, line)
    fd.puts line
  end

  def put_message(fd, msg)
    fd.puts msg + EOM_TOKEN
  end

  def broadcast(msg)
    @client_fd.map { |cli|
      put_message(cli, msg)
    }
  end

  def get_line(fd)
    fd.gets.chomp
  end

  def close
    @server.close
    @client_fd.each { |fd| fd.close }
    @client_fd.clear
  end
end # Fish_Server

# class Player
#   attr_reader :fd, :name, :hand, :next_hand_number

#   def initialize(name="", fd, hand)
#     @next_hand_to_assign = @next_hand_number ? @next_hand_number + 1 : 0
#     @name = "Unknown Player #{next_hand_number}" if name == ""
#     @fd = fd
#     @hand = hand
#   end
# end # Player
