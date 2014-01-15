require_relative "../Player.rb"

describe Player, "Player communications" do
  it ".new creates an empty player" do
    player = Player.new(0, "No Name")
    
    player.number.should eql 0
    player.name.should eql "No Name"
  end

  it ".tell, sends a message for the player" do
    player = Player.new()
    player.tell("message one")
    player.tell("message two")

    player.messages?.should eql true
  end

  it ".messages, returns an array of outstanding messages for the player" do
    player = Player.new()
    player.tell("message one")
    player.tell("message two")

    messages = player.messages(false)

    messages[0].should eql "message one"
    messages[1].should eql "message two"
    messages[2].should eql nil

    player.messages?.should eql true
  end

  it ".messages, returns the array of outstanding messages for the player, and deletes them" do
    player = Player.new()
    player.tell("message one")

    messages = player.messages(true)

    messages[0].should eql "message one"
    messages[1].should eql nil

    player.messages?.should eql false
  end
end
