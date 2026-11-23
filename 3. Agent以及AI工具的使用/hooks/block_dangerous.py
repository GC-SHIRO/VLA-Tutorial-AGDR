"""PreToolUse Hook：在工具执行前检查命令，拦截明显危险的操作。

输入：从 stdin 读取一个 JSON，至少包含 tool_name 和 tool_input
      （与 Claude Code 传给 Hook 的格式一致）
输出：退出码 0 表示放行；退出码 2 表示阻止，stderr 的内容会作为原因反馈给模型

注意：这只是用字符串匹配做的「安全网」，很容易被绕过，不能代替人工确认和隔离环境。
"""
import json
import re
import sys

RULES = [
    (r"\brm\s+-[a-zA-Z]*[rf]", "禁止使用 rm -r / rm -f 批量删除文件"),
    (r"\bsudo\b", "禁止使用 sudo"),
    (r"(curl|wget)[^|]*\|\s*(ba|z)?sh", "禁止把下载的内容直接交给 shell 执行"),
    (r"\bchmod\s+(-R\s+)?777\b", "禁止把权限设为 777"),
    (r"\bgit\s+reset\s+--hard\b", "禁止 git reset --hard"),
]


def main():
    event = json.load(sys.stdin)
    command = (event.get("tool_input") or {}).get("command", "")
    for pattern, reason in RULES:
        if re.search(pattern, command):
            print(f"被安全 Hook 阻止：{reason}。命令：{command}", file=sys.stderr)
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
