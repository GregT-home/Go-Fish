#!/usr/bin/ruby
require_relative "./fishserver.rb"

def stack_deck
  puts "Creating the test deck"
  test_hand_size = 7
  number_of_test_hands = 2
  target_hand, stacked_deck = [],[]
  target_hand[0] = "2C 2H 3C QH 5C 4H 9H".split
  target_hand[1] = "2S 2D 3S 3D 5S 4D 9C".split
  target_hand[2] = "10C 10H 10S 10D AC AH 9S".split
  test_hand_size.downto(0) { |card_num| 
    number_of_test_hands.times { |hand_num|
      stacked_deck << target_hand[hand_num][card_num]
    }
  }

  extra_cards = "3H".split
  extra_cards.map { |card_string| stacked_deck << card_string }

  stacked_cards_string = stacked_deck.join(" ")
  test_deck = Card.new_cards_from_s(stacked_cards_string)

end

# take # of players from command line, if present
num = ARGV.length > 0 ? ARGV[0].to_i : 0

# get it from terminal, if not in command line
until num >= 1 && num <= 10
  print "How many players for this game (2-10)? "
  num = gets.chomp.strip.to_i
end

test_deck = stack_deck

puts "Creating a Fish Server for #{num} players..."
server = FishServer.new(num, test_deck)
server.debug

server.run

server.close
