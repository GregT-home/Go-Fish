require_relative '../../GoFish_app'
require 'rspec/expectations'
require 'spinach/capybara'
#require capybara/poltergeist'

Spinach::FeatureSteps.send(:include, Spinach::FeatureSteps::Capybara)
Capybara.app = GoFishApp

require_relative './helpers'

Spinach.hooks.before_scenario do
  LoginScreen.reset
  GoFishApp.reset
end

Spinach.hooks.after_scenario do
  ::Capybara.reset_sessions!
  ::Capybara.use_default_driver
end

