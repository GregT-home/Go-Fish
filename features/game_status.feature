Feature: Game Status
As a player in the game

  In order to understand what is going on and what strategies I need
  to make, I need to know who is playing, how many cards they are
  holding, how many cards are in the pond and what the results of the
  most recent turn were.

  Scenario: Dashboard information display
  Given I am a registered user
  When the game begins
  And I look in the status area
       Then I can see how many cards remain in the pond
       Then I can see whose turn it is now
       Then I can see each of my oppoonents
       Then I can see how many cards each of my opponents has
       Then I can see how many books each of my opponents has
