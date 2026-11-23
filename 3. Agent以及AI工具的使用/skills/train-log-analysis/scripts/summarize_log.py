"""统计本实验室格式的训练日志。用法：python3 summarize_log.py <日志文件>"""
import re
import sys
from collections import Counter


def main():
    if len(sys.argv) != 2:
        print("用法: summarize_log.py <日志文件>", file=sys.stderr)
        sys.exit(1)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"文件不存在: {sys.argv[1]}", file=sys.stderr)
        sys.exit(2)

    losses = []  # (epoch, loss)
    levels = Counter()
    errors = Counter()
    for line in lines:
        level = re.match(r"\[(\w+)\]", line)
        if level:
            levels[level.group(1)] += 1
        found = re.search(r"epoch=(\d+) loss=([\d.]+)", line)
        if found:
            losses.append((int(found.group(1)), float(found.group(2))))
        if line.startswith("[ERROR]"):
            errors[line.split(maxsplit=1)[1] if " " in line else "unknown"] += 1

    print(f"epochs={len(losses)}")
    if losses:
        best_epoch, best_loss = min(losses, key=lambda x: x[1])
        print(f"best_loss={best_loss} best_epoch={best_epoch}")
        print(f"last_loss={losses[-1][1]} last_epoch={losses[-1][0]}")
    print(f"warn={levels['WARN']} error={levels['ERROR']}")
    if errors:
        name, count = errors.most_common(1)[0]
        print(f"top_error={name} count={count}")


if __name__ == "__main__":
    main()
