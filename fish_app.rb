require 'sinatra'
require 'slim'

get '/' do
    slim :fish_dashboard
end
