class Player
  attr_reader :number, :name, :hand, :socket

  def initialize(number, name, hand, socket)
    @number = number
    @name = name
    @hand = hand
    @socket = socket
  end

end #Player
