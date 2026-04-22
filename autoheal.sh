#!/usr/bin/env bash

URL="http://localhost:8000/"
LOG="./autoheal.log"
INTERVAL=30

while true; do
    if ! curl -sf --max-time 5 "$URL" > /dev/null 2>&1; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[$TIMESTAMP] Service unavailable — restarting via docker compose..." | tee -a "$LOG"
        docker compose restart 2>&1 | tee -a "$LOG"
    fi
    sleep "$INTERVAL"
done
