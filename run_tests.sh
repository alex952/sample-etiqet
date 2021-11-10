#!/bin/bash

set -e

pushd ./etiqet-demo
mvn clean test
popd
