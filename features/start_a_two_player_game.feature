@start-2
Feature: Start a Two-Player Game
As a prospective player

  In order to provide a pleasant user experience I want to allow the
  first user in a game to decide how many players can play and
  subsequent players join the game in progress.

  Scenario: First player registers for a game
 	Given a potential player
	And he is the first player to the game
	When he identifies himself by name to the server
	Then he chooses to create a game for two players
	And he clicks on the 'start' button
	Then he is registered for the game and goes to the game page
	And the game is not started
	And a second player comes to the game
	And he joins an existing game
	When he identifies himself by name to the server
	And he clicks on the 'start' button
	Then he is registered for the game and goes to the game page
	And the game begins
