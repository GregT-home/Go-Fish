require_relative "../Player.rb"

describe Player, "Player communications" do
  before (:each) do
    @player = Player.new(0, "No Name")
  end

  it ".new creates an empty human player" do
    expect(@player.number).to eql 0
    expect(@player.name).to eql "No Name"
    class Player
      attr_reader :type
    end
    expect(@player.type).to be(:human)
  end

  it "#make_robot changes the player type" do
    class Player
      attr_reader :type
    end
    expect(@player.type).to be(:human)
    @player.make_robot
    expect(@player.type).to be(:robot)
  end

  it "#robot? is true if the player is a robot" do
    @player.make_robot
    expect(@player.robot?).to be true
  end

  it "#make_human changes the player type" do
    @player.make_robot
    @player.make_human
    expect(@player.type).to be(:human)
  end

  it "#robot? is false if the player is not a robot" do
    expect(@player.robot?).to be false
  end

  it ".tell, sends a message for the player" do
    @player.tell("message one")
    @player.tell("message two")

    expect(@player.messages?).to be true
  end

  it ".messages, returns an array of outstanding messages for the player" do
    @player.tell("message one")
    @player.tell("message two")

    messages = @player.messages(false)

    expect(messages[0]).to eql "message one"
    expect(messages[1]).to eql "message two"
    expect(messages[2]).to be nil

    expect(@player.messages?).to be true
  end

  it ".messages, returns the array of outstanding messages for the player, and deletes them" do
    @player.tell("message one")

    messages = @player.messages(true)

    expect(messages[0]).to eql "message one"
    expect(messages[1]).to be nil

    expect(@player.messages?).to be false
  end
end
