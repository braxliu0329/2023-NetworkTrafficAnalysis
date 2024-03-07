#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

monitor=false
promiscuous=false
analysis=false
if [[ $# -gt 2 ]]
then
    cat "$DIR/help.txt"
    exit
fi
for arg in "$@"; do
    case "$arg" in
        "--analysis")
            if [[ $# -eq 2 && ("$2" != "--monitor" && "$2" != "--promiscuous") ]]
            then
                echo "Usage: $0 [--analysis] [--monitor | --promiscuous]"
                exit
            fi
            analysis=true
            cd "$DIR/src/analysis/backend" || exit
            
            ./nta10a &
            cd $DIR || exit
            ;;
        "--monitor")
            if [[ $# -eq 2 && "$2" = "--promiscuous" ]]
            then
                echo "You cannot enable both monitor mode and promiscuous mode"
                echo "Usage: ./run.sh [--analysis][--monitor | --promiscuous]"
                exit
            if [[ $# -eq 2 && "$2" != "--analysis" ]]
            then
                    echo "Usage: ./run.sh [--analysis][--monitor | --promiscuous]"
                    exit
                fi
            fi
            monitor=true
            ;;
        "--promiscuous")
            if [[ $# -eq 2 && "$2" = "--monitor" ]]
            then
                echo "You cannot enable both monitor mode and promiscuous mode"
                echo "Usage: $0 [--analysis][--monitor | --promiscuous]"
                exit
            if [[ $# -eq 2 && "$2" != "--analysis" ]]
            then
                    echo "Usage: $0 [--analysis][--monitor | --promiscuous]"
                    exit
                fi
            fi
            promiscuous=true
            ;;
        "--help")
            cat "$DIR/help.txt"
            exit;;
        "--version")
            echo "1.0a"
            exit;;
        *)
            cat "$DIR/help.txt"
            exit;;
    esac
done

python3 "$DIR/src/main.py" "$analysis" "$promiscuous" "$monitor"


