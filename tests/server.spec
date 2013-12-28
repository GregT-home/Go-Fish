require_relative "../FishServer.rb"
require_relative "../FishClient.rb"
require "socket"

describe FishServer, "receives from, and sends to clients" do
  context ".new: Create a test server and two client connections" do
    # create a standard server
    before (:each) do
      @server = FishServer.new

      @client1 = FishClient.new("localhost")
      @client2 = FishClient.new("localhost")
      
      # clients send to server first, for test purposes.
      # first answer is the name of the player
      test_msg1 = "client 1: Player One"
      test_msg2 = "client 2: Player Two"
      @client2.send_line test_msg2
      @client1.send_line test_msg1

      @c1fd = @server.accept_client
      @c2fd = @server.accept_client
      @server.clients.length.should == 2

      msg = @server.get_line(@c1fd)
      msg.should == test_msg1
      msg = @server.get_line(@c2fd)
      msg.should == test_msg2
    end

    # close when done
    after (:each) do
      @server.close
      @client1.close
      @client2.close
    end

    it "can welcome a client connection" do

      welcome_message = <<EOM
Welcome to the Fish Server

EOM
      @server.put_message(@c1fd, welcome_message)

      msg =  @client1.receive_message
      msg.should == welcome_message
    end

    it "can request and receive a player name" do
      prompt = "What is your name: "
      @server.put_message(@c1fd, prompt)
      response =  @client1.receive_message
      response.should == prompt

      name_msg = "Player One"
      @client1.send_line(name_msg)

      msg =  @server.get_line(@c1fd)
      msg.should == name_msg
    end      

    it "can broadcast to all connected clients" do
      bcast_msg="This is a broadcast message\nTesting 1, 2, 3\n"
      @server.broadcast(bcast_msg)

      [@client1, @client2].map { |cli|
        client_sees = cli.receive_message
        client_sees.should == bcast_msg
      }
    end      


  end # context
end # FishServer

