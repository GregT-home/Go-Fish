@play
Feature: Game Play
As a player in the game whose turn it is

  I need to be able ask any of my opponents whether they have any of the cards I possess.

  Scenario: Ask Request
    Given I am a registered user
    When it is my turn
    And I look in the action-area
      Then I can see a pull-down list of the players I can ask for cards.
      Then I can see a pull-down list of the cards I can request.
      Then I can see an "Ask" button to press to initiate my request.
      When I select a player from the pull-down list
      And I select a card from the pull-down list
      And I hit the "Ask" button
      Then I see a game response in the history-area

