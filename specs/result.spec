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

      expect(result.requester).to eql @game.current_player
      expect(result.victim).to eql 1
      expect(result.rank).to eql "3"
      expect(result.matches).to eql 0
      expect(result.received_from_player).to eql nil
      expect(result.received_from_pond).to eql nil
      expect(result.book_made).to eql nil
      expect(result.game_over).to eql false

      expect {result.requester = 1}.to raise_error NoMethodError
      expect {result.victim = 2}.to raise_error NoMethodError
      expect {result.rank = 3}.to raise_error NoMethodError
    end

    it "A Round Results can have its values changed." do
      result = Result.new(@game.current_player, 1, "3")

      expect {result.requester = 1}.to raise_error NoMethodError
      expect {result.victim = 2}.to raise_error NoMethodError
      expect {result.rank = 3}.to raise_error NoMethodError
      result.matches                 = 4
      result.received_from_player    = true
      result.book_made               = false
      result.game_over               = 6

      expect(result.requester).to            eql @game.current_player
      expect(result.victim).to               eql 1
      expect(result.rank).to                 eql "3"
      expect(result.matches).to              eql 4
      expect(result.received_from_player).to eql true
      expect(result.book_made).to            eql false
      expect(result.game_over).to            eql 6
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
      result.received_from_pond = true
      result.book_made = false
      result.game_over = false

      expect(result.to_s).to eq test_string
    end

    it "case 2: ask Victim: gets; Pond: N/A; Book: N/A; plays again." do
      test_string =<<EOF
Player got 2.
He did not make a book.
EOF
      test_string = test_string.chomp

      result = Result.new(0,1,"3")
      result.matches = 2
      result.received_from_player = true
      result.book_made = false
      result.game_over = false

      expect(result.to_s).to eq test_string
    end

    it "case 3: ask Victim: gets; Pond: N/A; Book: Yes; plays again." do
      test_string =<<EOF
Player got 2.
He made a book of 2s.
EOF
      test_string = test_string.chomp

      result = Result.new(0,1,"2")
      result.matches = 2
      result.received_from_player = true
      result.book_made = true
      result.game_over = false

      expect(result.to_s).to eq test_string
    end

    it "case 4: ask Victim: no get; Pond: get; Book: no; plays again." do
      test_string =<<EOF
Player was told to 'Go Fish' and he got one from the pond!
He did not make a book.
EOF
      test_string = test_string.chomp

      result = Result.new(0,2,"3")
      result.matches = 1
      result.received_from_pond = true
      result.book_made = false
      result.game_over = false

      expect(result.to_s).to eq test_string
    end

    it "case 5: ask Victim: no get; Pond: get; Book: yes; plays again." do
      test_string =<<EOF
Player was told to 'Go Fish' and he got one from the pond!
He made a book of 3s.
EOF
      test_string = test_string.chomp

      result = Result.new(0,2,"3")
      result.matches = 1
      result.received_from_pond = true
      result.book_made = true
      result.game_over = false

      expect(result.to_s).to eq test_string
    end
    
    it "case 6: ask Victim: no get; Pond: get; Book: yes--surprise; next player." do
      test_string =<<EOF
Player was told to 'Go Fish' and he got one from the pond!
He was surprised to make a book of 3s.
EOF
      test_string = test_string.chomp

      result = Result.new(0,2,"Q")
      result.matches = 1
      result.received_from_pond = true
      result.book_made = true
      result.surprise_rank = "3"
      result.game_over = false

      expect(result.to_s).to eq test_string
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
      result.received_from_player = nil
      result.received_from_pond = nil
      result.book_made = false

      result.game_over = true

      expect(result.to_s).to eq test_string
    end
  end # to_s tests
end # round results creation/manipulation
