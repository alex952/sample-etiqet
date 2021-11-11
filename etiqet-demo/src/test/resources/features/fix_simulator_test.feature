Feature: FIX Simulator test

  Scenario: Logon Example
    Given a "fix" client
    And filter out "Logon" message
    When client is logged on
    Then send a "Heartbeat" message
    And stop client

Scenario: Send a NewOrderSingle and receive 3 reports back
    Given a "fix" client
    When client is logged on
    And filter out "Logon" message
    Then send a "NewOrderSingle" message with "ClOrdID=99,Symbol=EURUSD,Side=1,OrderQty=100,OrdType=2,Price=3.3" as "order"
    Then wait for an "ExecutionReport" message as "ackBuy"
    Then wait for an "ExecutionReport" message as "ackAcceptBuy"
    Then wait for an "ExecutionReport" message as "FillBuy"
    Then check that "OrderID" in "ackBuy" is not equal to "OrderID" in "FillBuy"
    Then check that "LeavesQty" in "ackBuy" is not equal to "LeavesQty" in "FillBuy"
    Then check that "LeavesQty" in "FillBuy" is less than "OrderQty" in "FillBuy"
    Then stop client

Scenario: Send a OrderCancelRequest and receive 2 reports back
    Given a "fix" client
    When client is logged on
    And filter out "Logon" message
    Then send a "OrderCancelRequest" message with "OrigClOrdID=1,ClOrdID=99,Symbol=EURUSD,Side=1" as "cancelReq"
    Then wait for an "ExecutionReport" message as "pendingCancel"
    Then wait for an "ExecutionReport" message as "Cancel"
    Then stop client

Scenario: Send a OrderCancelReplaceRequest and receive 3 reports back
    Given a "fix" client
    When client is logged on
    And filter out "Logon" message
    Then send a "OrderCancelReplaceRequest" message with "OrigClOrdID=1,ClOrdID=99,Symbol=EURUSD,Side=1,OrderQty=100,OrdType=2,Price=3.3" as "replaceReq"
    Then wait for an "ExecutionReport" message as "pendingReplace"
    Then wait for an "ExecutionReport" message as "Replace"
    Then stop client

