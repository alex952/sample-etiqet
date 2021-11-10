Feature: FIX Simulator test

  Scenario: Logon Example
    Given a "fix" client
    And filter out "Logon" message
    When client is logged on
    Then send a "Heartbeat" message
    And stop client

Scenario: Check that a fix message value is greater than another fix message value
    Given a "fix" client
    When client is logged on
    And filter out "Logon" message
    Then send a "NewOrderSingle" message with "ClOrdID=99,Symbol=EURUSD,Side=1,OrderQty=100,OrdType=1" as "order"
    Then wait for an "ExecutionReport" message as "ackBuy"
    Then wait for an "ExecutionReport" message as "ackAcceptBuy"
    Then wait for an "ExecutionReport" message as "FillBuy"
    Then check that "OrderID" in "ackBuy" is not equal to "OrderID" in "FillBuy"
    Then check that "LeavesQty" in "ackBuy" is not equal to "LeavesQty" in "FillBuy"
    Then check that "LeavesQty" in "FillBuy" is less than "OrderQty" in "FillBuy"
    Then stop client

