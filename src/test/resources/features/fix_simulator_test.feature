Feature: FIX Simulator test

  Scenario: Logon Example
    Given a "fix" client
    And filter out "Logon" message
    When client is logged on
    Then send a "Heartbeat" message
    And stop client

