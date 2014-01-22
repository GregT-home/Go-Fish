require 'sinatra/base'
require 'pry'
require 'slim'
require_relative './game'
require 'pusher'
require_relative './app_login'

# Pusher['test_channel'].trigger('my_event', {
#   message: 'hello world'
# })

# enable pretty formatting for development.  Remove for production.
Slim::Engine.default_options[:pretty] = true

class GoFishApp < Sinatra::Base
#  disable :show_exceptions
  @@games = {}
  Pusher.url = "http://7e6cd02d8eb61aab0534:4e766c545fdbe5f59114@api.pusherapp.com/apps/63932"

  def self.reset
    @@games = {}
  end

  def self.games
    @@games
  end

  def self.send_refresh(game_id)
    Pusher[game_id.to_s].trigger('refresh', { message: 'refresh' })
  end

  use LoginScreen # middleware will run before filters

  before do
    unless session['user_name']
      halt "You are not a known user.<br><br>" +
        "<a href='/login'>Please register and login</a>."
    end
  end

  get '/' do
    @game = @@games[session['game_id']]

    if session['number_of_players']
      @number_of_players = session['number_of_players']
    end

    if @game.number_of_hands == @number_of_players
      puts "--","Game is starting with #{@game.number_of_hands} hands."
      @game.start_game
    end

    player_number = session['player_number']
    hand = @game.player_number_to_hand(player_number)

    if false
      puts "**** List of hands:"
      @game.hands.each do |hand|
        player=@game.owner(hand)
        puts "**** cards: #{player.number}) #{player.name}: #{hand.to_slim}"
      end
      puts "**** game's current hand: #{@cards}"
      puts "**** current hand: #{@cards}"

      player_number = session['player_number']
      hand = @game.player_number_to_hand(player_number)
      @cards = hand.to_slim
      puts "==== your hand: #{@cards}"
    end

    def bundle_players(game)
      players = {}
      game.hands.each do |hand|
        owner = game.owner(hand)
        players[owner.number] = {
          name: owner.name,
          hand: hand,
          books: game.books_to_slim(hand),
          books_count: game.number_of_books(hand),
          books_string: game.books_to_s(hand),
          number_of_cards: hand.count
        }
      end
      players
    end
    def bundle_info(game)
      info={}
      info['current_player_number'] = game.current_player.number
      info['current_player_name'] = game.current_player.name
      info['number_of_players'] = game.number_of_players
      info['current_hand'] = @game.current_hand.to_slim.split
      if game.started
        info['pond_size'] = game.pond_size
      else
        info['pond_size'] = 0
      end
      info
    end

    @info = bundle_info(@game)
    @players = bundle_players(@game)
    @messages = @game.owner(@game.current_hand).messages(true)


#    slim :fish_dashboard, locals:{ info: info, players: players, messages: messages }
    slim :fish_dashboard
  end

# it is likely that we need a post route that contains, among other
# things, this trigger:
#    GoFishApp.send_refresh(@game.object_id)


# run the GoFishApp if we are invoked directly
run! if app_file == $0
end



