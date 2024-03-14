#!/bin/bash

cd src/analysis/backend
echo "Building server..."
GO="/usr/local/go/bin/go"
$GO build -o nta10a main.go
echo "Finished server build"
cd ../App
echo "Building webpage..."
yarn build