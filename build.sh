#!/bin/bash

cd src/analysis/backend
echo "Building server..."
GO="/usr/local/go/bin/go"
$GO build -o nta10 main.go
cd ../App
yarn build