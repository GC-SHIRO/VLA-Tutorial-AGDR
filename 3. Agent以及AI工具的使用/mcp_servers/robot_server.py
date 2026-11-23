"""一个最小的 MCP server：只用 Python 标准库，通过 stdio 通信。

第 04 节用它讲解 MCP 协议。它提供两个工具：
- list_robots：列出实验室的机器人
- query_robot_battery：查询某台机器人的电量（数据是假的）

通信规则（MCP 的 stdio 传输方式）：
- 客户端把本程序作为子进程启动，通过 stdin 发消息，通过 stdout 收消息
- 每条消息是一行 JSON-RPC 2.0 格式的 JSON
- stdout 只能用来输出协议消息；日志必须写到 stderr，否则会破坏通信

也可以把它接入真实的 Agent，例如 Claude Code：
    claude mcp add robot -- python3 <本文件的绝对路径>
"""
import json
import sys

SERVER_INFO = {"name": "agdr-robot", "version": "0.1.0"}
SUPPORTED_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"]

ROBOTS = {
    "so100-01": {"battery_percent": 87, "location": "工位 A"},
    "so100-02": {"battery_percent": 23, "location": "工位 B"},
}

TOOLS = [
    {
        "name": "list_robots",
        "description": "列出实验室里所有机器人的编号和位置",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "query_robot_battery",
        "description": "查询实验室某台机器人的当前电量（百分比）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "robot_id": {"type": "string", "description": "机器人编号，例如 so100-01"},
            },
            "required": ["robot_id"],
        },
    },
]


def log(*args):
    # 日志写到 stderr；写到 stdout 会被客户端当作协议消息
    print("[robot_server]", *args, file=sys.stderr, flush=True)


def text_result(text, is_error=False):
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def call_tool(name, arguments):
    if name == "list_robots":
        lines = [f"{rid}（{info['location']}）" for rid, info in ROBOTS.items()]
        return text_result("\n".join(lines))
    if name == "query_robot_battery":
        robot_id = arguments.get("robot_id", "")
        if robot_id not in ROBOTS:
            # 工具执行失败：仍然是一个正常的响应，只是 isError 为 true，让模型看到错误
            return text_result(f"找不到机器人 {robot_id}", is_error=True)
        data = {"robot_id": robot_id, "battery_percent": ROBOTS[robot_id]["battery_percent"]}
        return text_result(json.dumps(data, ensure_ascii=False))
    raise KeyError(name)


def handle(message):
    """处理一条请求，返回 result；不认识的方法抛出 NotImplementedError"""
    method = message.get("method")
    params = message.get("params") or {}

    if method == "initialize":
        requested = params.get("protocolVersion")
        version = requested if requested in SUPPORTED_VERSIONS else SUPPORTED_VERSIONS[0]
        return {
            "protocolVersion": version,
            "capabilities": {"tools": {}},  # 声明：我提供工具
            "serverInfo": SERVER_INFO,
        }
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        return call_tool(params.get("name"), params.get("arguments") or {})
    raise NotImplementedError(method)


def send(message):
    sys.stdout.write(json.dumps(message) + "\n")  # 一条消息一行
    sys.stdout.flush()


def main():
    log("已启动，等待客户端消息")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        message = json.loads(line)
        if "id" not in message:
            # 没有 id 的是通知（notification），不需要回复
            log("收到通知", message.get("method"))
            continue
        log("收到请求", message.get("method"))
        try:
            send({"jsonrpc": "2.0", "id": message["id"], "result": handle(message)})
        except NotImplementedError as error:
            send({"jsonrpc": "2.0", "id": message["id"],
                  "error": {"code": -32601, "message": f"Method not found: {error}"}})
        except KeyError as error:
            send({"jsonrpc": "2.0", "id": message["id"],
                  "error": {"code": -32602, "message": f"Unknown tool: {error}"}})
    log("stdin 已关闭，退出")


if __name__ == "__main__":
    main()
