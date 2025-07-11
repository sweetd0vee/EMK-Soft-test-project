#!/bin/bash

. env.sh

export COMPOSE_PROJECT_NAME=shop

docker-compose -f docker-compose.yml up -d
