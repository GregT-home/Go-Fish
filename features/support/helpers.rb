# Re-open class and add a few helper methods
class Spinach::FeatureSteps
  def helper_get_game(current_scope)
     game_id = current_scope.session.driver.request.session['game_id']
     game = GoFishApp.games[game_id]
 end
  def helper_show_page
      save_and_open_page("tmp-pagedump.html")
  end

  def helper_check_sinatra_failure
    debug = false
    if page.html.length > 10000
      puts "Saving and opening page" if debug
      save_and_open_page("tmp-pagedump.html")
    else
      puts "generated HTML is #{page.html.length} characters long." if debug
    end
    #    expect(page.html.length).to be < 10000
    expect(page).not_to have_content("BACKTRACE")
  end
end

# Re-open class and add a few helper methods
class Capybara::Session
  def helper_has_card?(card)
    has_css?("img[alt=\"#{card.to_s}\"]")
  end
end

class Helper

end
