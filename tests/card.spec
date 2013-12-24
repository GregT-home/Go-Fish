#Dir['../tests/*.rb'].each { |file| require_relative "#{file}" }
require_relative "../card.rb"

describe Card, ".new: cards can be created." do
  it "They have rank and suit." do
    card1 = Card.new('A','C')
    card2 = Card.new('A','H')
    
    card1.rank.should eql card2.rank
    card1.suit.should_not eql card2.suit
  end
end # cards can be created

describe Card, ".new cards have a value as well as a rank and suit.." do
  it "holds a card rank and suit, can be compared exactly, and can compare value" do
    card1 = Card.new('10','C')
    card1same = Card.new('10','C')
    card2eq_rank = Card.new('10','H')
    card3higher = Card.new('A','S')
    card4lower = Card.new('2','D')
    
    card1.should == card1same
    card1.should_not == card2eq_rank
    card1.value.should == card2eq_rank.value

    card1.value.should eql card2eq_rank.value
    
    card1.suit.should_not eql card2eq_rank.suit
    card3higher.value.should be > card1.value
    card4lower.value.should  be < card1.value
  end
end # Pcard can be compared

describe Card, ".new: cards can be generated from rank/suit strings." do
  it ".new: can be done one or more times" do
    static_cards = [Card.new('A','C'),
                    Card.new('2','C'),
                    Card.new('3','C') ]

    cards = Card.new_cards_from_s("A-C 3C 4c")

    cards.each { |card|
      card.is_a?(Card).should == true
      }
  end

  it ".new_cards_from_string: a single card can be created" do
    card = Card.new_cards_from_s("2-H")[0]
    card.is_a?(Card).should == true
  end
end # Can be created from strings
