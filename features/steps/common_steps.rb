module CommonSteps
  module Register
    include Spinach::DSL
    step 'I am a registered user' do
      visit "/login"
      within(".Login")do
        fill_in 'user_name', :with => "Test Person"
        click_on 'Submit'
      end
    end
  end
end
