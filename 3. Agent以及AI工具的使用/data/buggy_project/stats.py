"""训练日志统计工具"""


def best_loss(path):
    """返回日志中最低的 loss"""
    losses = []
    for line in open(path, encoding="utf-8"):
        if "loss=" in line:
            losses.append(line.split("loss=")[1].strip())
    return min(losses)
