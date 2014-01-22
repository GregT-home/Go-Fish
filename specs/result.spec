require_relative "../card.rb"
require_relative "../deck.rb"
require_relative "../hand.rb"
require_relative "../game.rb"
require_relative "../result.rb"

describe Result, "Round Result creation and manipulation." do
  context "Round results need an active game." do
    before (:each) do
      @game = Game.new()
      @game.add_player(1, "Test Player")
      @game.start_game()
    end

    it "A Round Result can be created." do
      result = Result.new(@game.current_player, 1, "3")

      result.requester.should == @game.current_player
      result.victim.should == 1
      result.rank.should == "3"
      result.matches.should == 0
      result.received_from.should == nil
      result.books_made.should == 0
      result.game_over.should == false

      expect {result.requester = 1}.to raise_error
      expect {result.victim = 2}.to raise_error
      expect {result.rank = 3}.to raise_error
    end

    it "A Round Results can have its values changed." do
      result = Result.new(@game.current_player, 1, "3")

      expect {result.requester = 1}.to raise_error
      expect {result.victim = 2}.to raise_error
      expect {result.rank = 3}.to raise_error
      result.matches                 = 4
      result.received_from           = :some_one
      result.books_made              = 5
      result.game_over               = 6

      result.requester.should       == @game.current_player
      result.victim.should          == 1
      result.rank.should            == "3"
      result.matches.should         == 4
      result.received_from.should   == :some_one
      result.books_made.should      == 5
      result.game_over.should       == 6
    end
  end #context

  context ".to_str" do
    it "case 1: ask Victim: none; Pond: Yes; Book: N/A; turn over." do
      test_string =<<EOF
Player was told to 'Go Fish' and he got one from the pond!
He did not make a book.
EOF
      test_string = test_string.chomp

      result = Result.new(0,2,"3")
      result.matches = 1
      result.received_from = :pond
      result.books_made = 0
      result.game_over = false

      result.to_s.should eq test_string
    end

    it "case 2: ask Victim: gets; Pond: N/A; Book: N/A; plays again." do
      test_string =<<EOF
Player got 2.
He did not make a book.
EOF
      test_string = test_string.chomp

      result = Result.new(0,1,"3")
      result.matches = 2
      result.received_from = 1
      result.books_made = 0
      result.game_over = false

      result.to_s.should eq test_string
    end

    it "case 3: ask Victim: gets; Pond: N/A; Book: Yes; plays again." do
      test_string =<<EOF
Player got 2.
He made a book of 2s.
EOF
      test_string = test_string.chomp

      result = Result.new(0,1,"2")
      result.matches = 2
      result.received_from = 1
      result.books_made = 1
      result.game_over = false

      result.to_s.should eq test_string
    end

    it "case 4: ask Victim: no get; Pond: get; Book: no; plays again." do
      test_string =<<EOF
Player was told to 'Go Fish' and he got one from the pond!
He did not make a book.
EOF
      test_string = test_string.chomp

      result = Result.new(0,2,"3")
      result.matches = 1
      result.received_from = :pond
      result.books_made = 0
      result.game_over = false

      result.to_s.should eq test_string
    end

    it "case 5: ask Victim: no get; Pond: get; Book: yes; plays again." do
      test_string =<<EOF
Player was told to 'Go Fish' and he got one from the pond!
He made a book of 3s.
EOF
      test_string = test_string.chomp

      result = Result.new(0,2,"3")
      result.matches = 1
      result.received_from = :pond
      result.books_made = 1
      result.game_over = false

      result.to_s.should eq test_string
    end
    
    it "case 6: ask Victim: no get; Pond: get; Book: yes--surprise; next player." do
      test_string =<<EOF
Player was told to 'Go Fish' and he got one from the pond!
He was surprised to make a book of 3s.
EOF
      test_string = test_string.chomp

      result = Result.new(0,2,"Q")
      result.matches = 1
      result.received_from = :pond
      result.books_made = 1
      result.surprise_rank = "3"
      result.game_over = false

      result.to_s.should eq test_string
    end
    
    it "end case: ask Victim: no get; Pond: get; Book: yes; plays again." do
      test_string =<<EOF
Player was told to 'Go Fish' and he did not get what he asked for from the pond.
He did not make a book.
The Game is now over
EOF
      test_string = test_string.chomp

      result = Result.new(0,2,"3")
      result.matches = 0
      result.received_from = nil
      result.books_made = 0
      result.game_over = true

      result.to_s.should eq test_string
    end
  end # to_s tests
end # round results creation/manipulation
