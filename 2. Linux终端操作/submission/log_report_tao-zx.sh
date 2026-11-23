#!/bin/bash
# analyze_log.sh

if [ "$#" -ne 1 ]; then
    echo "用法： $0 <日志文件路径>" >&2
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "错误：日志文件不存在或不是一个文件" >&2
    exit 2
fi

log="$1"
lines=$(wc -l < "$log")
info=$(grep -c "INFO" "$log")
warn=$(grep -c "WARN" "$log")
error=$(grep -c "ERROR" "$log")
best_line=$(grep -o 'step=[0-9]* loss=[0-9.]*' "$log" | sort -t= -k3 -n | head -1)
best_step=$(echo "$best_line" | grep -o 'step=[0-9]*' | cut -d= -f2)
best_loss=$(echo "$best_line" | cut -d= -f3)
top_error=$(grep "ERROR" "$log" | awk '{print $4}' | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')

echo "lines: $lines"
echo "info: $info"
echo "warn: $warn"
echo "error: $error"
echo "best_loss: $best_loss"
echo "best_step: $best_step"
echo "top_error: $top_error"

exit 0