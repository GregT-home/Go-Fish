#Dir['../tests/*.rb'].each { |file| require_relative "#{file}" }
require_relative "../PlayingCard.rb"
#require_relative "../CardUtils.rb"

describe PlayingCard, "Playing cards can be created with rank and suit." do
  it "Create cards and verify we can see rank and suit." do
    card1 = PlayingCard.new('A','C')
    card2 = PlayingCard.new('A','H')
    
    card1.rank.should eql card2.rank
    card1.suit.should_not eql card2.suit
  end
end # Pcards can be created

describe PlayingCard, "Playing cards created with invalid ranks and suits are flagged as exceptions." do
  it "Create a card with an invalid rank." do
    expect { PlayingCard.new('REALLY WRONG','C') }.to raise_error(RuntimeError)
  end

  it "Create a card with an invalid rank." do
    expect { PlayingCard.new('5', 'REALLY WRONG') }.to raise_error(RuntimeError)
  end
end # Bad suit or rank raises exception

describe PlayingCard, "Playing cards can be compared by rank, suit or value." do
  it "holds a card rank and suit, can be compared exactly, and can compare rank or suit" do
    card1 = PlayingCard.new('10','C')
    card1same = PlayingCard.new('10','C')
    card2eq_rank = PlayingCard.new('10','H')
    card3higher = PlayingCard.new('A','S')
    card4lower = PlayingCard.new('2','D')
    
    card1.should == card1same
    card1.should_not == card2eq_rank
    card1.rank.should == card2eq_rank.rank

    card1.rank.should eql card2eq_rank.rank
    
    card1.suit.should_not eql card2eq_rank.suit
    card3higher.rank.should be > card1.rank
    card4lower.rank.should  be < card1.rank
  end
end # Pcard can be compared

describe PlayingCard, "Playing cards can be generated from a specification string." do
  it "can be done one or more times" do
    static_cards = [PlayingCard.new('A','C'),
                    PlayingCard.new('2','C'),
                    PlayingCard.new('3','C') ]

    cards = PlayingCard.cards_from_string("A-C 3C 4c")

    cards.each { |card|
      card.is_a?(PlayingCard).should == true
      }
  end

  it "can be done for a single card" do
    card = PlayingCard.cards_from_string("2-H")[0]
    card.is_a?(PlayingCard).should == true
  end
end # Can be created from strings
