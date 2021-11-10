#!/bin/bash

set -e

pushd ./quickfix-server
python server.py server.cfg
popd
