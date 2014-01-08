require 'sinatra'
require 'slim'

Slim::Engine.default_options[:pretty] = true

get '/' do
    slim :fish_dashboard
end
