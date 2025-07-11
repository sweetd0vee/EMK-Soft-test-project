#!/usr/bin/env bash

IMAGE=arina/shop
TAG=master

cd ..

docker build -t $IMAGE:$TAG .

