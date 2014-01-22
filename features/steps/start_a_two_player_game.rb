#tag @start-2
class Spinach::Features::StartATwoPlayerGame < Spinach::FeatureSteps

@debug=true

  step 'a potential player' do
    visit "/login"
    helper_check_sinatra_failure
    expect(current_path).to eql("/login")
    expect(page).to have_content("Please enter your Player Name:")
  end

  step 'a second player comes to the game' do
    ::Capybara.session_name = :second_player
    visit "/login"
    helper_check_sinatra_failure
    expect(current_path).to eql("/login")
    expect(page).to have_content("Please enter your Player Name:")
  end

  step 'he identifies himself by name to the server' do
    # in same page
    log "adding Test Person ##{@player_number}"
    find('.Registration').fill_in('user_name', :with => "Test Person ##{@player_number}")
  end

  step 'he is the first player to the game' do
    @player_number = 1
    expect(page).to have_content("How many players will be playing")
  end

  step 'he joins an existing game' do
    @player_number = 2
    expect(page).to have_content("You will be joining an existing game")
    end

  step 'he chooses to create a game for two players' do
    helper_check_sinatra_failure
    find('.Registration').fill_in('number_of_players', :with => "2")
  end

  step 'he clicks on the \'start\' button' do
    find(".Registration").click_on('Start')
  end

  step 'he is registered for the game and goes to the game page' do
    expect(page).to have_content("Your Cards")
  end

  step 'the game is not started' do
    game_id = current_scope.session.driver.request.session['game_id']
    game = GoFishApp.games[game_id]
    expect(game).not_to be nil
    expect(game.started).to be false
  end

  step 'the game begins' do
    game_id = current_scope.session.driver.request.session['game_id']
    game = GoFishApp.games[game_id]
    expect(game).not_to be nil
    expect(game.started).to be true
    helper_check_sinatra_failure
  end

  def log(message)
    puts "log: #{message}"  if @debug
  end

  # def game
  #   if @game
  #     game_id = current_scope.session.driver.request.session['game_id']
  #     @game = GoFishApp.games(game_id)
  #   else
  #     @game
  #   end
  # end

end
