require 'sinatra/base'
require 'pry'
require 'slim'
require_relative "./game"

# enable pretty formatting for development.  Remove for production.
Slim::Engine.default_options[:pretty] = true

# Get the user's player name
class LoginScreen < Sinatra::Base
  enable :sessions     # makes Sinatra create a session hash
  @@usernames = {}

  get('/login') do
    # if we have a user_name, there is no need to log in again
    if session['user_name']
      redirect "/"
    else
puts @@usernames.count
      slim :login, locals:{number_of_players:  @@usernames.count }
    end
  end

  post('/login') do
    if params[:user_name].strip.empty?
      redirect '/login'    # no user_name? Push them back to the login page.
    else
      #code will not work,  need way to get last hash entry.
      user_id = @@usernames.count + 1

      session['user_name'] = params[:user_name]
      session['user_id'] = user_id
    end

    # create game, if needed
    if GoFishApp.games.count == 0
      game = Game.new()
      GoFishApp.games[game.object_id] = game
    else
      game = GoFishApp.games.values[0]
    end

    session['game_id'] = game.object_id
    game.add_hand()
    player = Player.new(user_id, params[:user_name])
    game.add_player(player)
    @@usernames[player] = params[:user_name]
    redirect '/'
  end
end # LoginScreen

class GoFishApp < Sinatra::Base
  @@games = {}

  def self.games
    @@games
  end

  use LoginScreen # middleware will run before filters


  before do
    unless session['user_name']
      halt "#{session.inspect}<br><br>" +
        "You are not a known user.<br><br>" +
        "<a href='/login'>Please register and login</a>."
    end
  end

  get '/' do
    @game = @@games[session['game_id']]

    if session['user_name'].downcase == "debug" ||
        session['user_name'].downcase == "debug2"
      binding.pry
    end

    if session['user_name'].downcase == "start"
      puts "--","Game is starting with #{@game.number_of_hands} hands."
      @game.start_game
    end

    @cards = %w{5h 6d 6s 9c 9s kd kh ks}.map { |e| e.downcase}
    @books = %w{7 J 8}
    # reminder params['players'] from Login page contains the results of the form

    slim :fish_dashboard
  end

# run the GoFishApp if we are invoked directly
run! if app_file == $0
end



