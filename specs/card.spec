# Jan-2014: Test(s) need to be added for == and related hash equivalence operators.

#Dir['../tests/*.rb'].each { |file| require_relative "#{file}" }
require_relative "../card.rb"
require_relative "./testhelp.rb"

describe Card, ".new: cards can be created." do
  it "They have rank and suit." do
    card1 = Card.new('A','C')
    card2 = Card.new('A','C')
    
    expect(card1.rank).to eql card2.rank
    expect(card1.suit).to eql card2.suit
  end
end # cards can be created

describe Card, ".new cards have a value as well as a rank and suit." do
  it "equal, but different, cards are equal" do
    ten_clubs = Card.new('10','C')
    ten_clubs2 = Card.new('10','C')
    expect(ten_clubs).to eq ten_clubs2
end

  it "higher rank is greater than lower" do
    card = Card.new('10','H')
    card_higher = Card.new('A','S')
    expect(card_higher.value).to be > card.value
  end

  it "lower rank is less than higher" do
    card = Card.new('10','C')
    card_lower = Card.new('2','D')
    
    expect(card_lower.value).to be < card.value
  end
end # Pcard can be compared

describe TestHelp, ".new: cards can be generated from rank/suit strings." do
  it ".new: can be done one or more times" do
    static_cards = [Card.new('A','C'),
                    Card.new('2','C'),
                    Card.new('3','C') ]
    expect(static_cards[0].rank).to eql "A"
    expect(static_cards[0].suit).to eql "C"
    expect(static_cards[1].rank).to eql "2"
    expect(static_cards[1].suit).to eql "C"
    expect(static_cards[2].rank).to eql "3"
    expect(static_cards[2].suit).to eql "C"
  end

  it ".card_from_s: a card can be created from string" do
    card = TestHelp.cards_from_hand_s("A-C")[0]
    expect(card.rank).to eql "A"
    expect(card.suit).to eql "C"
  end

  it ".card_from_s: multiple cards can be created from string" do
    cards = TestHelp.cards_from_hand_s("A-C 3C 4c")

    cards.each { |card|
      expect(card.is_a?(Card)).to eq true
      }
  end

  it ".cards_from_hand_s: a single card can be created and represented as a string" do
    card = TestHelp.card_from_s("2-H")
    expect(card.is_a?(Card)).to eq true
    expect(card.to_s).to eq "2-H"
  end


end # Can be created from strings
