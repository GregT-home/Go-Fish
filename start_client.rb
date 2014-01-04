#!/usr/bin/ruby
require_relative "./fishserver.rb"
require_relative "./fishclient.rb"

welcome = <<EOF
Welcome to the Fish Server

Play will begin when all the players have joined the game.  Please Wait.

When the game begins, you will be notified and the players will be listed.
When it is your turn, you may request a rank from any player in any of
the following ways:

   Player 1 do you have any 3s?
   1 3?

If your input is not understood you will be asked to provide it again.

Now, to begin...

EOF

def get_server_name(args)
  server_name = args.length > 0 ? args[0] : nil

  while server_name.nil?
    print "What is the name of your server (default: 'localhost')? "
    server_name = gets.chomp.strip
    server_name = "localhost" if server_name.empty?
  end
  puts "server name is #{server_name}"
  server_name
end

def connect_to_server(args)
  server_name = get_server_name(args)

  begin
    puts "Creating FishClient to #{server_name}"
    client = FishClient.new(server_name); break

  rescue Errno::ECONNREFUSED, SocketError => reason
    puts "#{server_name} error: #{reason.to_s}"
    server_name = nil
  ensure
    args = nil
  end while server_name = get_server_name()
  client
end


# Does not block, displays any messages coming in from the server

print welcome

client = connect_to_server(ARGV)

client.display_server_messages

while true do
  begin
    client.send_line(STDIN.gets.chomp)
    client.socket.recv(0)
  rescue Errno::ECONNRESET
    puts "The Server has closed the connection unexpectedly"
    break
  rescue NoMethodError
    puts "Client termination requested."
    break
  end
end

puts "exiting..."
