class Spinach::Features::IdentifyPlayer < Spinach::FeatureSteps
  step 'a first time user' do
    #pending 'step not implemented'
    # non-false return marks this as done in Spinach
    
  end

  step 'they identify themselves by name' do
#    pending 'step not implemented'
    visit "/login"
    within(".About")do
      fill_in 'user_name', :with => "Test Person"
      click_on 'Submit'
    end
    
    
end

  step 'they\'re successfully associated with a new game and redirected to the game page.' do
#    pending 'step not implemented'
    page.should have_content("Your Cards")
  end
end
