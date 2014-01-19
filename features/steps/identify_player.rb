class Spinach::Features::IdentifyPlayer < Spinach::FeatureSteps
  step 'a potential player' do
    visit "/login"
    expect(page).not_to have_content("BACKTRACE")
    expect(current_path).to eql("/login")
    expect(page).to have_content("Please enter your Player Name:")
  end

  step 'he identifies himself by name to the server' do
    # in same page
puts "adding Test Person ##{@player_number}"
    find('.Registration').fill_in('user_name', :with => "Test Person ##{@player_number}")
  end

  step 'he is the first player to the game' do
    @player_number = 1
    expect(page).to have_content("How many players will be playing")
  end

  step 'he is the second player to the game' do
    @player_number = 2
    expect(page).to have_content("You will be joining an existing game")
    end

  step 'he must choose how many players will play the new game' do
    expect(page).not_to have_content("BACKTRACE")
    find('.Registration').fill_in('number_of_players', :with => "1")
  end

  step 'he clicks on the \'start\' button' do
    find(".Registration").click_on('Start')
  end

  step 'he is associated with the current game and is redirected to the game page.' do
    expect(page).to have_content("Your Cards")
  end
end
