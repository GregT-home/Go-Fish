class Player
  attr_reader :name, :hand, :socket

  def initialize(name, hand, socket)
    @name = name
    @hand = hand
    @socket = socket
  end

end #Player
