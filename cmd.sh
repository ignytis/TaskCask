#!/usr/bin/env bash

set -eu

command="$1"
shift;
case "$command" in
    "test" )
        pytest;;
    "exec" )
        tcask $@;;
esac
