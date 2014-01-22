#!/usr/bin/ruby
require_relative "./fishserver.rb"
require_relative "./specs/testhelp.rb"

def stack_deck
  cards = TestHelp.cards_from_hand_s("QH 9H 5C 4H 3C 2C 2H",
                                     "9C 5S 4D 3S 3D 2S 2D",
                                     "AC AH 9S 10C 10H 10S 10D")
  cards.unshift(TestHelp.card_from_s("3H"))
  cards
end

# def stack_deck
#   puts "Creating the test deck"
#   test_hand_size = 7
#   number_of_test_hands = 2
#   target_hand, stacked_deck = [],[]
#   target_hand[0] = "2C 2H 3C QH 5C 4H 9H".split
#   target_hand[1] = "2S 2D 3S 3D 5S 4D 9C".split
#   target_hand[2] = "10C 10H 10S 10D AC AH 9S".split
#   test_hand_size.downto(0) do |card_num| 
#     number_of_test_hands.times  do |hand_num|
#       stacked_deck << target_hand[hand_num][card_num]
#     end
#   end

#   extra_cards = "3H".split
#   extra_cards.map { |card_string| stacked_deck << card_string }

#   stacked_cards_string = stacked_deck.join(" ")
#   test_deck = Card.new_cards_from_s(stacked_cards_string)

# end

# take # of players from command line, if present
# also use a stacked deck, if requested
num = ARGV.count > 0 ? ARGV[0].to_i : 0
use_stacked_deck = true if ARGV[1] == "stack" or ARGV[1] == "test"
puts "Using stacked deck." if use_stacked_deck == true

# get it from terminal, if not in command line
until num >= 1 && num <= 10
  print "How many players for this game (2-10)? "
  num = gets.chomp.strip.to_i
end

if use_stacked_deck
  puts "Using a deck stacked for the standard 3 players."
  test_deck = stack_deck
end

puts "Creating a Fish Server for #{num} players..."
server = FishServer.new

<><>

# This code musst be re-worked to work with new game paradigm shift
# from hands to players

(num, test_deck)
server.debug

server.run

server.close
