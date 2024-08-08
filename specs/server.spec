require_relative "../fishserver.rb"
require "socket"


#Hand_str_regexp = Regexp.new("\[|10|[2-9]|[JQKA]|-[CDHS]]", true)

class MockClient
  attr_reader :socket

  def initialize(hostname='localhost',port=FishServer::PORT)
    @debug = false
    log "calling MockClient.new(#{hostname},#{port})"
    @socket = TCPSocket.open(hostname,port)
    send_line("Hello") # initiate contact with the server
    receive_line

  end

  def send_line(string)
    log "calling send_line(#{string})"
    @socket.puts string
  end

  def consume_message
    log "calling consume_message"
    message = ""
    begin
      message += receive_line + "\n"
      if /:EOM:/.match(message)
        message[FishServer::EOM_TOKEN+"\n"]=""
        break
      end
      log "  (consumed #{message})"
    end while true
  end

  def receive_message
    log "calling receive_message"
    message = ""
    begin
      message += receive_line + "\n"
      if /:EOM:/.match(message)
        message[FishServer::EOM_TOKEN+"\n"]=""
        break
      end
    end while true
    log "receive_message returning: #{message}"
    message
  end

  def close
    log "closing #{socket.inspect}"
    @socket.close
  end

  def debug
    @debug = ! @debug
  end

private
  def receive_line
    @socket.gets.chomp
  end

  def log(message)
    STDOUT.puts "Client Log: " + message if @debug
  end

end # MockClient


def helper_accept_clients(server, number)
  thread_id = Thread.new do
    while server.client.count < number do
      server.accept_client
    end
  end
end

describe FishServer, "Initialization" do
  it "#new: can create a server" do
    server = FishServer.new

    expect(server.is_a?(FishServer)).to be true
    expect(server.game.is_a?(Game)).to be true
    server.close
  end 
end # end .new


describe FishServer, "#get_clients." do
  it "accepts multiple clients" do
    server = FishServer.new
    server.game.add_player(1, "Test Player 1")
    server.game.add_player(2, "Test Player 2")

    # kick-off a non-blocking server thread
    helper_accept_clients(server, 2)

    client1=MockClient.new
    client2=MockClient.new

    expect(server.client.count).to eq 2

    client1.close
    client2.close
    server.close
  end
end # .get_clients

describe FishServer, "#put_message" do
  it "can send a message to a specific client" do
    server = FishServer.new
    server.game.add_player(1, "Test Player 1")

    # kick-off a non-blocking server thread
    helper_accept_clients(server, 1)

    name = "Player One's Name"
    mclient = MockClient.new

    #sending name first for test purposes (avoids blocking)
    mclient.send_line(name)

    welcome_message = <<EOM
    Welcome to the Fish Server

EOM
    server.put_message(server.client[0], welcome_message)
    msg = mclient.receive_message.strip

    expect(msg).to eq welcome_message.strip

    mclient.close
    server.close
  end
end # .put_message

describe FishServer, "#broadcast." do
  it "can send a message to all clients" do
    server = FishServer.new
    server.game.add_player(1, "Test Player 1")

    # kick-off a non-blocking server thread
    helper_accept_clients(server, 2)

    name1 = "Player One's Name"
    name2 = "Player Two's Name"
    mclient1=MockClient.new
    mclient2=MockClient.new

    expect(server.client.count).to eq 2

    #sending name first for test purposes (avoids blocking)
    mclient1.send_line(name1)
    mclient2.send_line(name2)

    welcome_message = <<EOM
    Welcome to the Fish Server

EOM
    server.broadcast(welcome_message)

    msg = mclient1.receive_message.strip
    expect(msg).to eq welcome_message.strip

    msg = mclient2.receive_message.strip
    expect(msg).to eq welcome_message.strip

    mclient1.close
    mclient2.close
    server.close
  end
end # .broadcast
