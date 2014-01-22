@status
Feature: Game Status
As a player in the game

  In order to understand what is going on and what strategies I need
  to make, I need to know who is playing, how many cards they are
  holding, how many cards are in the pond and what the results of the
  most recent turn were.

  Scenario: Dashboard information display
  Given player is registered and starts a two person game
  
  When the second player joins the game
  And the game begins
  And player one looks in the status area
    Then he can see how many cards remain in the pond
    And he can see whose turn it is
    And he can see each of his opponents
    And he can see how many cards each of his opponents has
    And he can see how many books each of his opponents has
    And he can see the results of the last turn
    And he can see his own hand
    And he can see his own books
