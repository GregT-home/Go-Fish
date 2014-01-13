require_relative '../../GoFish_app'
require 'rspec/expectations'
require 'spinach/capybara'

Spinach::FeatureSteps.send(:include, Spinach::FeatureSteps::Capybara)
#Capybara.app = Sinatra::Application
Capybara.app = GoFishApp
