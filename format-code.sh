#!/usr/bin/env bash

command -v yapf &> /dev/null || {
    echo "yapf is required to format the code"
    exit 127
}

yapf -i test/**/*.py
