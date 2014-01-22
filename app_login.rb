# Get the user's player name
class LoginScreen < Sinatra::Base
  enable :sessions     # makes Sinatra create a session hash
  @@usernames = {}
  @@number_of_players = 0

  def self.reset
    @@usernames = {}
    @@number_of_players = 0
  end

  get('/login') do
    # if we have a user_name, there is no need to log in again
    if session['user_name']
      redirect "/"
    else
      slim :login, locals:{number_of_players:  @@usernames.count }
    end
  end

  post('/login') do
    if params[:user_name].strip.empty?
      redirect '/login'    # no user_name? Push them back to the login page.
    else
      player_number = @@usernames.count + 1
      session['user_name'] = params[:user_name]
      session['player_number'] = player_number

      if @@number_of_players > 0
        session['number_of_players'] = @@number_of_players
      else
        @@number_of_players =  params[:number_of_players].to_i
        session['number_of_players'] = @@number_of_players
      end
    end

    # create game, if needed
    if GoFishApp.games.count == 0
      game = Game.new()
      GoFishApp.games[game.object_id] = game
    else
      game = GoFishApp.games.values[0]
    end

    session['game_id'] = game.object_id
    game.add_player(player_number, params[:user_name])

    @@usernames[player_number] = params[:user_name]
    redirect '/'
  end
end # LoginScreen
