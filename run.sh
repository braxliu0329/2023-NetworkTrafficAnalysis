#! /bin/sh

cd src/analysis/backend
GO="/usr/local/go/bin/go"
$GO run main.go &
cd ../../../
python3 src/main.py

