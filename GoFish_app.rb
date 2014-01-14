require 'sinatra/base'
require 'pry'
require 'slim'
require_relative "./game"

# enable pretty formatting for development.  Remove for production.
Slim::Engine.default_options[:pretty] = true

# Get the user's player name
class LoginScreen < Sinatra::Base
  enable :sessions     # makes Sinatra create a session hash

  get('/login') {
    slim :login
  }

  post('/login') do
    unless params[:user_name].strip == ""
      session['user_name'] = params[:user_name]
      unless session.has_key?('game_id')
        game = Game.new(2)
        session['game_id'] = game.object_id
        GoFishApp.games[game.object_id] = game
      end
      redirect '/'
    else
      # if we got no user_name, then push them back to the login page.
      redirect '/login'
    end
  end
end # LoginScreen


class GoFishApp < Sinatra::Base
  use LoginScreen

  def self.games
    @@games ||= {}
  end

  before do
    unless session['user_name']
      halt "#{session.inspect}<br><br>Access denied, you are not registered.<br><br> <a href='/login'>Please register and login</a>."
    end
  end
  # middleware will run before filters

  get '/' do
    @game = @@games[session['game_id']]

    if session['user_name'].downcase == "debug"
      binding.pry
    end

    @cards = %w{5h 6d 6s 9c 9s kd kh ks}.map { |e| e.downcase}
    @books = %w{7 J 8}
    slim :fish_dashboard
  end
end



