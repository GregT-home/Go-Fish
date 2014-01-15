class Player
  attr_reader :number, :name, :hand, :socket

  def initialize(number = nil, name = nil, socket = nil)
    @number = number
    @name = name
    @socket = socket
    @messages = []
  end

  def tell (msg)
    @messages << msg
  end

  def messages (consume = false)
    messages = @messages
    @messages = [] if consume
    messages
  end

  def messages?
    !@messages.empty?
  end

end #Player

