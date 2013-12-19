require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../fish_hand.rb"

describe Fish_Game, "Multi-player Game of Fish" do

  context "Initial game setup: Create deck and 6 hand." do
    before (:each) do
      @deck = Deck.new
      @deck.length.should == 52

      # create stacked hands
      hand[0] = Fish_Hand(Card.new_cards_from_string("2C 2H 3C 3H 4C 4H"))  
      hand[1] = Fish_Hand(Card.new_cards_from_string("2S 2D 3S 3D 4S 4D"))
      hand[2] = Fish_Hand(Card.new_cards_from_string("5S 5D 6S 6D 7S 7D"))
      hand[3] = Fish_Hand(Card.new_cards_from_string("5C 5H 6C 6H 7C 7H"))  
      hand[4] = Fish_Hand(Card.new_cards_from_string("10S 10D JS JD AS AD"))
      hand[5] = Fish_Hand(Card.new_cards_from_string("10C 10H JC JH AC AH"))

      # remove cards in hands from the deck
      hand.map { |hand|
        hand.cards { |target_card|
          @deck.cards { |card|
            begin
              card = @deck.give_card
              @dec.receive_card(card) unless card != target_card
            end
            }
          }
        }
      # deck should be lighter by 6 fidh hands
      @deck.length.should eql 52 - 6 * 6
      
      end
      	      
      @hand=FishHand.new()
    end

    
