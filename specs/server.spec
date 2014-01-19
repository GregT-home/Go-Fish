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

describe FishServer, "#new: can create a server" do
  it "#new: for one clients" do
    server = FishServer.new(1)
    server.number_of_players.should eq 1
    server.close
  end 

  it "#new: for two clients" do
    server = FishServer.new(2)
    server.number_of_players.should eq 2
    server.close
  end 
end # end .new

def accept_clients(server, number)
  thread_id = Thread.new do
    while server.client.count < number do
      server.accept_client
    end
  end
end

describe FishServer, "#get_clients." do
  it "accepts multiple clients" do
    server = FishServer.new(2)

    # kick-off a non-blocking server thread
    accept_clients(server, 2)

    client1=MockClient.new
    client2=MockClient.new

    server.client.count.should eq 2

    client1.close
    client2.close
    server.close
  end
end # .get_clients

describe FishServer, "#put_message" do
  it "can send a message to a specific client" do
    server = FishServer.new(1)

    # kick-off a non-blocking server thread
    accept_clients(server, 1)

    name = "Player One's Name"
    mclient = MockClient.new

    #sending name first for test purposes (avoids blocking)
    mclient.send_line(name)

    welcome_message = <<EOM
    Welcome to the Fish Server

EOM
    server.put_message(server.client[0], welcome_message)
    msg = mclient.receive_message.strip

    msg.should eq welcome_message.strip

    mclient.close
    server.close
  end
end # .put_message

describe FishServer, "#broadcast." do
  it "can send a message to all clients" do
    server = FishServer.new(1)

    # kick-off a non-blocking server thread
    accept_clients(server, 2)

    name1 = "Player One's Name"
    name2 = "Player Two's Name"
    mclient1=MockClient.new
    mclient2=MockClient.new

    server.client.count.should eq 2

    #sending name first for test purposes (avoids blocking)
    mclient1.send_line(name1)
    mclient2.send_line(name2)

    welcome_message = <<EOM
    Welcome to the Fish Server

EOM
    server.broadcast(welcome_message)

    msg = mclient1.receive_message.strip
    msg.should eq welcome_message.strip

    msg = mclient2.receive_message.strip
    msg.should eq welcome_message.strip

    mclient1.close
    mclient2.close
    server.close
  end
end # .broadcast
