#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "用法: $0 <日志文件路径>" >&2
    exit 1
fi

FILE="$1"
if [ ! -f "$FILE" ]; then
    echo "错误: 找不到文件 '$FILE'" >&2
    exit 2
fi

lines=$(wc -l < "$FILE")
info=$(grep -c '\[INFO\]' "$FILE" || true)
warn=$(grep -c '\[WARN\]' "$FILE" || true)
error=$(grep -c '\[ERROR\]' "$FILE" || true)

best_loss=$(grep -o 'loss=[0-9.]*' "$FILE" | cut -d= -f2 | sort -n | head -n 1)

best_step=$(grep 'loss=' "$FILE" | cut -d ' ' -f 5,6 | sed 's/step=//; s/loss=//' | sort -k2 -n | head -n 1 | cut -d ' ' -f 1)

top_error=$(grep '\[ERROR\]' "$FILE" | cut -d ' ' -f 4 | sort | uniq -c | sort -nr | head -n 1 | tr -s ' ' | cut -d ' ' -f 3)

echo "lines: $lines"
echo "info: $info"
echo "warn: $warn"
echo "error: $error"
echo "best_loss: $best_loss"
echo "best_step: $best_step"
echo "top_error: $top_error"

exit 0