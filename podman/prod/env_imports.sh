#!/bin/bash

# export $(grep -v '^#' .env.prod | xargs -d '\n')

NUM=$(grep -Eo '(^APPLICATION_PORT=)([0-9]+)' .env.prod | grep -Eo '[0-9]+')
echo "grepped this: $NUM"