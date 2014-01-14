require_relative "../fishclient.rb"

require "socket"

class MockServer
   PORT = 54011
   EOM_TOKEN = ":EOM:"

  attr_reader :client, :names, :players, :number_of_players, :game

  def initialize(number)
    @client = []
    @players = []
    @number_of_players = number
    @game = nil

    @game = Game.new()
    number_of_players.downto(1) { @game.add_hand() }
    @game.start_game()

    @server = TCPServer.open(MockServer::PORT)	# listen on our port
  end

  def put_message(fd, msg)
    fd.puts msg + MockServer::EOM_TOKEN
  end

  def close
    @server.close
    @client.each { |fd| fd.close }
  end

  def get_clients
      while client.count < number_of_players
        client << @server.accept 
        #consume the "new player" response and let the client know
        put_line(client[-1], get_line(client[-1]))
      end
  end

  def get_line(fd)
    fd.gets.chomp
  end

  def put_line(fd, line)
    fd.puts line
  end

end # MockServer

 describe FishClient, "can connect to, receive and send to Server." do
  context "Create a one-player mock server" do
    # create a standard server
    before (:each) do
      num_players = 1
      @mock_server = MockServer.new(num_players)
      @mock_server.number_of_players.should eq num_players

      # kick-off a non-blocking server thread
      thread_id = Thread.new { @mock_server.get_clients }
    end

    # close when done
    after (:each) do
      @mock_server.close
    end

    it ".new: can create a socket connection to a running server." do
      client = FishClient.new

      @mock_server.client.count.should == 1

      @mock_server.client[0].is_a?(TCPSocket).should be true
    end

    it ".send_line: can connect a single client and exchange messages." do
      client = FishClient.new

      # client sends to server first, for test purposes.
      test_message = "Client: Hello"
      client.send_line test_message

      cfd = @mock_server.client[0]
      msg = @mock_server.client[0].gets.chomp
      msg.should eql test_message
    end

    it ".get_line: can receive a single-line from the server." do
      client = FishClient.new

      test_line = "Client: this is a test"

      @mock_server.put_line(@mock_server.client[0], test_line)
      line = client.receive_line

      line.should == test_line
    end

    it ".get_message: can receive a multi-line message from the server." do
      client = FishClient.new

      mline_test_msg = "Client:\nthis\nis\n\n\na\ntest1"

      @mock_server.put_message(@mock_server.client[0], mline_test_msg)
      msg = client.receive_message

      msg.should == mline_test_msg
    end
  end # context
end # client.spec

