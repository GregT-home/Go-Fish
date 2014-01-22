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

    if @game.number_of_players == @number_of_players
      puts "--","Game is starting with #{@game.number_of_players} players."
      @game.start_game
    else
      puts "--","Game now has #{@game.number_of_players} players."
    end

    player_number = session['player_number']

    @my = @game.player_from_number(player_number)
    @current_player = @game.current_player

    slim :fish_dashboard
  end

# it is likely that we need a post route that contains, among other
# things, this trigger:
#    GoFishApp.send_refresh(@game.object_id)


# run the GoFishApp if we are invoked directly
run! if app_file == $0
end



