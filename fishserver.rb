require_relative "./game.rb"
require_relative "./player.rb"
require 'socket'

class FishServer
  # rspec reports these as being re-defined; unless clause inhibits this.
  PORT = 54011        unless const_defined?(:PORT)
  EOM_TOKEN = ":EOM:" unless const_defined?(:EOM_TOKEN)
  Help_string =<<-EOF
  Choices are:
    ask <player #> for <rank>
    deck size
    hand
    status
EOF

  attr_reader :client, :names, :players, :number_of_players, :game

  def initialize(number, test_deck = nil)
    @client = []
    @players = []
    @number_of_players = number
    @game = nil
    @debug=false

    log "Creating a game"
    @game = Game.new()
    log "Adding #{number_of_players} hands"
    number_of_players.downto(1) { @game.add_hand() }
    log "starting the game (test_deck = #{test_deck})"
    @game.start_game(test_deck)

    @server = TCPServer.open(PORT)	# listen on our port
    log "Listening for connections on #{PORT}"
  end


  def accept_client
    @client << @server.accept 
    log "accept_clients: accepting a new client, now have #{@client.count}"
    #consume the "new player" response and let the client know
    client.last.puts get_line(client.last)
  end

  # get name, associate
  def create_players
    0.upto(number_of_players - 1) do |i|
      begin
        put_message(client[i], "What is your name? ")
        name = get_line(client[i]).strip
      end while name.empty?

      player = Player.new(i+1, name, @game.current_hand, client[i])
      players << player
      put_message(player.socket,
                  "Your cards: #{player.hand.to_s}\n")
      @game.advance_to_next_hand
    end
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
