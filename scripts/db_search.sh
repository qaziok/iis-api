#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No search phrase set, usage: $0 [PHRASE]"
else
    docker compose run --rm api python -m src.db_search "$1"
fi
