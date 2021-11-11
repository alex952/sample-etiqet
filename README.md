# Etiqet demo project
The repository contains:

* Simple python quickfix acceptor that will reply to NewOrderSingle/OrderCancelRequest/OrderCancelReplaceRequest messages (found in _quickfix-server_)
* Java project implementing tests using Etiqet (found in _etiqet-demo_)

Features for test definitions are located under *src/test/resources/features*

## Running the project
Some scripts were created to run the setup.

* **run_server.sh**: this will run the quickfix server
* **run_tests.sh**: this will compile and run the Etiqet tests
* **run_all.sh**: this will run the above consecutively and exit all processes when tests are done
