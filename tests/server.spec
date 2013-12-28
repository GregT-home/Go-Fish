require_relative "../FishServer.rb"
require_relative "../FishClient.rb"
require "socket"

class MockServer
  attr_reader :clients

  def initialize()
    @clients = []
    @server = TCPServer.open(FishServer::PORT)	# listen on our port
  end

  def accept_client
    clients << @server.accept
    clients[-1]
  end

  def put_line(fd, line)
    fd.puts line
  end

  def put_message(fd, msg)
    fd.puts msg + EOM_TOKEN
  end

  def get_line(fd)
    fd.gets.chomp
  end

  def close
    @server.close
    @clients.each { |fd| fd.close }
    @clients.clear
  end
end

describe FishClient, "receives from, and sends to clients" do
  context "Create a test server" do
    # create a standard server
    before (:each) do
      @mock_server = MockServer.new
    end

    # close when done
    after (:each) do
      @mock_server.close
    end

    it ".new: can create a socket connection to a running server." do
      client = FishClient.new

      client_fd = @mock_server.accept_client
      @mock_server.clients.count.should == 1

      client_fd.is_a?(TCPSocket).should be true
    end

    it ".send_line: can connect a single client and exchange messages." do
      client = FishClient.new

      # client sends to server first, for test purposes.
      test_message = "Client: Hello"
      client.send_line test_message

      client_list = @mock_server.accept_client
      cfd = @mock_server.clients[0]
      msg = cfd.gets
    end

    it ".send_line: can connect to multiple clients and exchange messages." do
      client1 = FishClient.new
      client2 = FishClient.new

      # client sends to server first, for test purposes.
      test_msg1 = "Client1: Hello"
      test_msg2 = "Client2: Hello"
      client2.send_line test_msg2
      client1.send_line test_msg1

      c1fd = @mock_server.accept_client
      c2fd = @mock_server.accept_client
      @mock_server.clients.length.should == 2

      msg2 = @mock_server.get_line(c2fd)
      msg1 = @mock_server.get_line(c1fd)

      msg1.should == test_msg1
      msg2.should == test_msg2
    end

    it ".get_message: can receive a multi-line message from the server." do
      client1 = FishClient.new

      # client sends to server first, for test purposes.
      hello_msg1 = "Client1: Hello"
      client1.send_line hello_msg1

      c1fd = @mock_server.accept_client
      @mock_server.clients.length.should == 1

      mline_test_msg1 = "Client1:\nthis\nis\na\ntest1\n"

      @mock_server.put_line(c1fd, mline_test_msg1+FishServer::EOM_TOKEN)
      msg1 = client1.receive_message

      msg1.should == mline_test_msg1
    end

    it ".get_message: can receive a multi-line message from the server." do
      client1, client2 = FishClient.new, FishClient.new

      # client sends to server first, for test purposes.
      hello_msg1 = "Client1: Hello"
      hello_msg2 = "Client2: Hello"
      client1.send_line hello_msg1
      client2.send_line hello_msg2

      c1fd = @mock_server.accept_client
      c2fd = @mock_server.accept_client
      @mock_server.clients.length.should == 2

      mline_test_msg1 = "Client1:\nthis\nis\na\ntest1\n"
      mline_test_msg2 = "Client2:\nthis\nis\na\ntest2\n"

      @mock_server.put_line(c1fd, mline_test_msg1+FishServer::EOM_TOKEN)
      msg1 = client1.receive_message
      @mock_server.put_line(c2fd, mline_test_msg2+FishServer::EOM_TOKEN)
      msg2 = client2.receive_message

      msg1.should == mline_test_msg1
      msg2.should == mline_test_msg2
    end

  end # context


end # FishServer

