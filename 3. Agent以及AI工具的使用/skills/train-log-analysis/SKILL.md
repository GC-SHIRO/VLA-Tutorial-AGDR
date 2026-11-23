---
name: train-log-analysis
description: 分析本实验室格式的训练日志（形如 "[INFO] epoch=1 loss=2.31" 的行），生成固定格式的训练报告。当用户要求分析训练日志、总结训练情况或排查训练异常时使用。
---

# 训练日志分析

## 步骤

1. 先运行统计脚本，不要自己逐行数，脚本的结果更准确：

   ```bash
   python3 .claude/skills/train-log-analysis/scripts/summarize_log.py <日志文件>
   ```

2. 根据脚本输出，按下面的模板写报告。模板里的每一项都要填，数字必须来自脚本输出。

## 报告模板

```text
## 训练报告：<日志文件名>

- epoch 数：<n>
- 最低 loss：<值>（epoch <n>）
- 最后一个 epoch 的 loss：<值>
- WARN：<次数>；ERROR：<次数>，最常见的是 <类型>（<次数> 次）

## 结论

<一两句话：loss 是否在下降；有没有需要处理的问题>
```

## 判断规则

- 最后一个 epoch 的 loss 高于最低值时，提醒用户考虑 early stopping，或改用最低 loss 对应的 checkpoint
- ERROR 中出现 `dataloader_timeout` 时，建议检查 `num_workers` 的设置和数据所在磁盘的读取速度
