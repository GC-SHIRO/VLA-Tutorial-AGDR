
#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <log_file>" >&2
    exit 1
fi

logFile="$1"

if [ ! -f "$logFile" ]; then
    echo "Error: File not found: $logFile" >&2
    exit 2
fi

lines=$(wc -l < "$logFile")
info=$(grep -c '\[INFO\]' "$logFile")
warn=$(grep -c '\[WARN\]' "$logFile")
error=$(grep -c '\[ERROR\]' "$logFile")

bestLoss=$(grep -o 'loss=[0-9.]*' "$logFile" | cut -d= -f2 | sort -n | head -n 1)

if [ -n "$bestLoss" ]; then
    bestStep=$(grep -F "loss=$bestLoss " "$logFile" | head -n 1 | grep -o 'step=[0-9]*' | cut -d= -f2)
else
    bestLoss="N/A"
    bestStep="N/A"
fi

topError=$(grep '\[ERROR\]' "$logFile" | cut -d' ' -f4 | sort | uniq -c | sort -rn | head -n 1 | tr -s ' ' | cut -d' ' -f3)

if [ -z "$topError" ]; then
    topError="N/A"
fi

echo "lines: $lines"
echo "info: $info"
echo "warn: $warn"
echo "error: $error"
echo "best_loss: $bestLoss"
echo "best_step: $bestStep"
echo "top_error: $topError"
