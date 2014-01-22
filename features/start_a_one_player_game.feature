@start-1
Feature: Start a One-Player Game
As a prospective player

  In order to provide a pleasant user experience I want to allow the
  first user in a game to decide how many players can play and
  to be able to play by himself.

  Scenario: First player registers for a game
 	Given a potential player
	And he is the first player to the game
	When he identifies himself by name to the server
	Then he chooses to create a game for one player
	And he clicks on the 'start' button
	Then he is registered for the game and goes to the game page
	And the game begins
  