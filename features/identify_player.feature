@id-player
Feature: Identify Player
As a prospective player

  In order to provide a pleasant user experience I want to allow the
  first user in a game to decide how many players can play and
  subsequent players join the game in progress.

  Scenario: First player registers for a game
 	Given a potential player
	And he is the first player to the game
	When he identifies himself by name to the server
	Then he must choose how many players will play the new game
	And he clicks on the 'start' button
	Then he is associated with the current game and is redirected to the game page.

  Scenario: Subsequent players register for games
 	Given a potential player
	And he is the second player to the game
	When he identifies himself by name to the server
	And he clicks on the 'start' button
	Then he is associated with the current game and is redirected to the game page.
  