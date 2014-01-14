require 'sinatra/base'
require 'pry'
require 'slim'
require_relative "./game"

# enable pretty formatting for development.  Remove for production.
Slim::Engine.default_options[:pretty] = true

# Get the user's player name
class LoginScreen < Sinatra::Base
  enable :sessions     # makes Sinatra create a session hash
  
  get('/login') { slim :login }

  post('/login') do
    unless params[:user_name].strip == ""
      # take the user name and stick it in the session.
      session['user_name'] = params[:user_name]
      @game = Game.new(2)
      session['game_id'] = @game.object_id
      GoFishApp.games[@game.object_id] = @game

      redirect '/'
    else
      # if we got no user_name, then push them back to the login page.
      redirect '/login'
    end
  end
end # LoginScreen

class GoFishApp < Sinatra::Base
  # middleware will run before filters
  use LoginScreen

  def self.games
    @@games ||= {}
  end


  before do
    unless session['user_name']
      halt "<br><br>Access denied, you are not registered.<br><br> <a href='/login'>Please register and login</a>."
    end
  end

  get '/' do

#    games << session['game_id']
#    @game = games[session['game_id']]

    if session['user_name'].downcase == "debug"
      binding.pry
    end

    @cards = %w{5h 6d 6s 9c 9s kd kh ks}.map { |e| e.downcase}
    @books = %w{7 J 8}
#    @game = @@game.first
    @game = Game.new(2)
    slim :fish_dashboard
  end
end



