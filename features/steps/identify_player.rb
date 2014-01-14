class Spinach::Features::IdentifyPlayer < Spinach::FeatureSteps
  step 'a first time user' do
    #pending 'step not implemented'
    # non-false return marks this as done in Spinach
    
  end

  step 'They identify themselves by name to the server' do
    visit "/login"
    within(".About")do
      fill_in 'user_name', :with => "Test Person"
      click_on 'Submit'
    end
  end

  step 'they\'re successfully associated with a new game and redirected to the game page.' do
    page.should have_content("Your Cards")
  end
end
