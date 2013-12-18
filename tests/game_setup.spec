#Dir['./*.rb'].each { |file| require_relative "#{file}" }
require_relative "./PlayingCard.rb"
require_relative "./CardDeck.rb"
require_relative "./FishPlayer.rb"

Test for "Happy Path"





describe CardDeck, "card deck" do
  it "deals all 52 cards to one player" do
    test_deck = CardDeck.new
    player=FishPlayer.new
    test_deck.deal([player])
    player.length.should eq 52

    52.times { card = player.get_next_card }
    card = player.get_next_card

    player.get_next_card.should eq nil
  end
end
