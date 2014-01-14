Feature: Identify Player
As the owner of the game

  In order to provide a pleasant user experience I want to identify a player in a friendly way before they play
  Scenario: Successful player identification
 	Given a first time user
	When they identify themselves by name to the server
	Then they're successfully associated with a new game and redirected to the game page.