#!/bin/bash

monitor=false
promiscuous=false
analysis=false
if [[ $# -gt 2 ]]
then
    cat help.txt
    exit
fi
for arg in "$@"; do
    case "$arg" in
        "--analysis")
            if [[ $# -eq 2 ]]
            then
                if [[ "$2" = "--help" || "$2" -eq "--version" ]]
                then
                    echo "Usage: ./run.sh [--analysis] [--monitor | --promiscuous]"
                    exit
                fi
            fi
            analysis=true
            cd src/analysis/backend
            GO="/usr/local/go/bin/go"
            $GO run main.go &
            cd ../../../
            ;;
        "--monitor")
            if [[ $# -eq 2 ]]
            then
                if [[ "$2" = "--promiscuous" ]]
                then
                    echo "You cannot enable both monitor mode and promiscuous mode"
                    echo "Usage: ./run.sh [--analysis][--monitor | --promiscuous]"
                    exit
                fi
            fi
            monitor=true
            ;;
        "--promiscuous")
            if [[ $# -eq 2 ]]
            then
                if [[ "$2" = "--monitor" ]]
                then
                    echo "You cannot enable both monitor mode and promiscuous mode"
                    echo "Usage: ./run.sh [--analysis][--monitor | --promiscuous]"
                    exit
                fi
            fi
            promiscuous=true
            ;;
        "--help")
            cat help.txt
            exit;;
        "--version")
            echo "1.0a"
            exit;;
    esac
done

python3 src/main.py

