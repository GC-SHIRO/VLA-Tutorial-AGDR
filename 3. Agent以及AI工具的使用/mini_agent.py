"""第 02 节写出的 mini agent，整理成一个模块，供后面的小节导入使用。

内容与 02-手写AgentLoop.ipynb 相同，只是去掉了讲解。建议先学完 02 节再看这个文件。
只使用 Python 标准库，OpenAI（Chat Completions）格式。
"""
import json
import os
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------- 配置

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "")
ONLINE = bool(OPENAI_API_KEY and OPENAI_MODEL)

SAMPLES = Path(__file__).resolve().parent / "data" / "samples"
WORKSPACE = (Path(tempfile.gettempdir()) / "agent-demo").resolve()
MAX_OUTPUT = 2000  # run_command 最多返回给模型的字符数


def show(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------- 调用模型

def post_json(url, headers, body):
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {error.code}: {detail}") from None


def call_model(messages, tools, offline_script):
    """调用一次模型。tools 为 None 时不提供工具。
    离线模式下，从 offline_script 里按顺序取出录制的响应。"""
    if not ONLINE:
        if not offline_script:
            raise RuntimeError("离线脚本已用完：离线模式只能运行教程预设的任务")
        sample = offline_script.pop(0)
        return json.loads((SAMPLES / sample).read_text(encoding="utf-8"))
    url = OPENAI_BASE_URL.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    body = {"model": OPENAI_MODEL, "messages": messages}
    if tools:
        body["tools"] = tools
    return post_json(url, headers, body)


# ---------------------------------------------------------------- 沙箱工作区

def setup_workspace():
    """重建沙箱工作区，放入一份模拟的训练日志"""
    shutil.rmtree(WORKSPACE, ignore_errors=True)
    WORKSPACE.mkdir()
    (WORKSPACE / "README.md").write_text(
        "# 机械臂抓取实验\n\n训练日志见 train.log，超参数见 config.json。\n", encoding="utf-8")
    (WORKSPACE / "config.json").write_text(
        '{"lr": 0.0003, "batch_size": 32, "epochs": 5}\n', encoding="utf-8")
    (WORKSPACE / "train.log").write_text(
        "[INFO] epoch=1 loss=2.31\n"
        "[WARN] gpu_memory_high\n"
        "[INFO] epoch=2 loss=1.87\n"
        "[ERROR] dataloader_timeout\n"
        "[INFO] epoch=3 loss=1.42\n"
        "[ERROR] camera_frame_dropped\n"
        "[INFO] epoch=4 loss=0.98\n"
        "[ERROR] dataloader_timeout\n"
        "[INFO] epoch=5 loss=1.05\n",
        encoding="utf-8",
    )
    return WORKSPACE


# ---------------------------------------------------------------- 工具

def safe_path(path):
    """把模型给的相对路径转成工作区内的绝对路径；越界就报错"""
    full = (WORKSPACE / path).resolve()
    if full != WORKSPACE and WORKSPACE not in full.parents:
        raise ValueError(f"不允许访问工作区之外的路径: {path}")
    return full


def list_dir(path="."):
    target = safe_path(path)
    names = sorted(p.name + ("/" if p.is_dir() else "") for p in target.iterdir())
    return "\n".join(names) or "(空目录)"


def read_file(path):
    return safe_path(path).read_text(encoding="utf-8")


def run_command(command):
    print(f"\n🤖 Agent 想在 {WORKSPACE} 中运行：\n    {command}")
    if input("允许执行吗？输入 y 执行，其他任意键拒绝：").strip().lower() != "y":
        return "用户拒绝执行这条命令。"
    completed = subprocess.run(
        command, shell=True, cwd=WORKSPACE,
        capture_output=True, text=True, timeout=30,
    )
    output = completed.stdout + completed.stderr
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + f"\n……（输出过长，已截断，共 {len(output)} 字符）"
    return f"退出码 {completed.returncode}\n{output}"


def tool_spec(name, description, properties, required):
    """生成一份 OpenAI 格式的工具说明书"""
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {"type": "object", "properties": properties, "required": required},
        },
    }


TOOL_SPECS = [
    tool_spec("list_dir", "列出工作区中某个目录下的文件，目录名以 / 结尾",
              {"path": {"type": "string", "description": "相对于工作区的路径，根目录是 ."}}, ["path"]),
    tool_spec("read_file", "读取工作区中一个文本文件的全部内容",
              {"path": {"type": "string", "description": "相对于工作区的文件路径"}}, ["path"]),
    tool_spec("run_command", "在工作区目录中运行一条 shell 命令，返回退出码和输出",
              {"command": {"type": "string", "description": "要运行的命令"}}, ["command"]),
]

TOOLS = {"list_dir": list_dir, "read_file": read_file, "run_command": run_command}


def execute_tool(name, arguments_json):
    try:
        args = json.loads(arguments_json)
        if name not in TOOLS:
            return f"错误：没有名为 {name} 的工具"
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"错误：{type(error).__name__}: {error}"


# ---------------------------------------------------------------- 循环

SYSTEM_PROMPT = """你是一个帮助分析机器人训练实验的助手。
你可以使用工具查看工作区中的文件。先用工具收集信息，再回答；不要猜测文件内容。
回答使用中文，简洁明了。"""


def print_step(step, reply, message):
    print(f"── 第 {step} 步 · 输入 {reply['usage']['prompt_tokens']} token")
    if message.get("content"):
        print("模型:", message["content"])


def run_tool_calls(tool_calls, messages):
    """执行一轮工具调用，把结果追加到 messages"""
    for call in tool_calls:
        name = call["function"]["name"]
        arguments = call["function"]["arguments"]
        print(f"调用工具: {name}({arguments})")
        result = execute_tool(name, arguments)
        preview = result if len(result) <= 120 else result[:120] + "……"
        print("工具结果:", preview.replace("\n", " | "))
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})


def run_agent(task, offline_script=None, max_steps=10):
    """02 节的 Agent Loop"""
    offline_script = list(offline_script or [])
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]
    for step in range(1, max_steps + 1):
        reply = call_model(messages, TOOL_SPECS, offline_script)
        choice = reply["choices"][0]
        message = choice["message"]
        messages.append(message)
        print_step(step, reply, message)

        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            if choice["finish_reason"] == "length":
                print("⚠️ 回答被截断了")
            return message.get("content"), messages
        run_tool_calls(tool_calls, messages)

    print(f"⚠️ 达到最大步数 {max_steps}，强制停止")
    return None, messages
