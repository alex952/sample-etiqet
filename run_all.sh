#!/bin/bash

set -e

./run_server.sh &
SERVER=$!
./run_tests.sh &
TESTS=$!
wait $TESTS
pkill -9 -P $SERVER
