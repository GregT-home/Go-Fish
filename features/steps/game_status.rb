# - make the books section a minimum size so that empty books don't
#   cause the screen to shrink markedly.
#
# - focus on the "easy" integrations and then figure out the harder ones:
#
# - give_player_status (and player.messages)
# 

require 'capybara/dsl'
class Spinach::Features::GameStatus < Spinach::FeatureSteps

  step 'player is registered and starts a two person game' do
    @player1_name = "Test Person #1"
    @player2_name = "Test Person #2"
    visit "/login"
    helper_check_sinatra_failure
    expect(page).to have_content("Please enter your Player Name:")
    log "adding Test Person ##{@player_number}"
    find('.Registration').fill_in('user_name', :with => @player1_name)
    expect(page).to have_content("How many players will be playing")
    within ('.Registration') do 
      fill_in 'number_of_players', :with => "2"
      click_on 'Start'
    end
    helper_check_sinatra_failure
    expect(page).to have_content("Your Cards")
#    expect(page).to have_content("Waiting for players")
  end

  step 'the second player joins the game' do
    ::Capybara.session_name = :player2
    visit "/login"
    helper_check_sinatra_failure
    expect(page).to have_content("You will be joining an existing game")
    within('.Registration') do
      fill_in 'user_name', :with => @player2_name
      click_on('Start')
    end
    helper_check_sinatra_failure
  end

  step 'the game begins' do
    ::Capybara.session_name = :player2
    expect(find "header").to have_content("(you are #{@player2_name})")
  end

  step 'player one looks in the status area' do
    ::Capybara.session_name = :default
    helper_check_sinatra_failure
    log ("visiting /login")
    helper_check_sinatra_failure
    visit "/login"
    expect(find ".hand-area").to have_content("Your Cards")
  end

  step 'he can see how many cards remain in the pond' do
    within(".pond") do
      expect(page.body).to match(/Pond has \d+ cards/)
      user_name = current_scope.session.driver.request.session['user_name']
      user_name.should eq(@player1_name)
      game = helper_get_game(current_scope)
      expect(game.started).to be true
      pond_size = game.deck.count

      expect(page).to have_content("Pond has #{pond_size} cards")
    end
  end

  step 'he can see whose turn it is' do
    expect(find(".status-area").text).to  match(/It is .*'s turn/)
    within(".status-area") do
      user_name = current_scope.session.driver.request.session['user_name']
      expect(user_name).to eq @player1_name
      game = helper_get_game(current_scope)
      pond_size = game.deck.count
      expect(page.body).to  match(/It is #{@player1_name}'s turn/)
    end
  end

  step 'he can see each of his opponents' do
    within(".status-area") do
      game = helper_get_game(current_scope)
      game.players_by_hand.each do |hand, player|
        puts "player number/name: #{player.number}/#{player.name}"
        expect(page.body).to match(/#{player.name} has/)
      end
    end
  end

  step 'he can see how many cards each of his opponents has' do
    within(".status-area") do
      game = helper_get_game(current_scope)
      game.players_by_hand.each do |hand, player|
        puts "player number/name: #{player.number}/#{player.name}"
        expect(page.body).to match(/#{player.name} has #{hand.count} cards/)
      end
    end
  end

  step 'he can see how many books each of his opponents has' do
    save_and_open_page("tmp-pagedump.html")
    within(".status-area") do
      game = helper_get_game(current_scope)
      game.players_by_hand.each do |hand, player|
        puts "player number/name: #{player.number}/#{player.name}"
        expect(page.text).to match(/#{player.name} has #{hand.count} cards/)
      end
    end
  end

  step 'he can see the results of the last turn' do
    within(".history-area") do
      game = helper_get_game(current_scope)
      messages = game.current_player.messages
      messages = messages.join("\n")
      # need beefier test case here, but not sure what/how to create it

      # currently, there are no messages in the player's buffer because
      # no turns have occurred.  Change game to put "Waiting for players"
      # in this spot for the first screen.
#      expect(messages).to match(/.*asked for .* from/)
    end
  end

  step 'he can see his own hand' do
    within(".status-area") do
      game = helper_get_game(current_scope)
      game.players_by_hand.each do |hand, player|
        puts "player number/name: #{player.number}/#{player.name}"
        expect(page.text).to match(/#{player.name} has #{hand.count} cards/)
      end
    end
  end

  step 'he can see his own books' do
    pending 'step not implemented'
  end

  def log(message)
    puts "log: #{message}"  if @debug
  end

end
