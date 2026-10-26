# AGDR VLA 入门教程

面向 AGDR 实验室新同学的 VLA（Vision-Language-Action）入门教学。目标不是直接上手模型，而是先补齐计算机基本功，再逐步走到机器人与 VLA 的论文和实战。

- 作者 / 维护者：Shiro
- 形式：交互式文档 + Jupyter Notebook（`.ipynb`）
- 特色：鼓励学习者全程使用 Claude Code 等 Agent 辅助学习，并把"如何高效使用 Agent"本身作为课程内容

> 状态：框架搭建中，各章节内容将逐步补全。目前已完成第 1 章。

## 你将学到什么

完成本教程后，你应当能够：

- 熟练使用 Git 进行协作开发
- 在 Linux 终端中完成日常开发与环境管理
- 使用 Agent / AI 工具辅助编程、查资料和排错
- 搭建 Python 机器学习环境，理解基本的 ML / 深度学习概念
- 了解 ROS2 与机器人运动学基础
- 使用 LeRobot 完成机器人学习实践
- 阅读 VLA 相关论文并复现 / 运行实战项目

## 目录结构

| 章节 | 目录 | 内容 |
| --- | --- | --- |
| 1 | `1. Git的使用与操作` | Git 基础、分支、协作流程（预计 1.5 小时） |
| 2 | `2. Linux终端操作` | Shell、文件系统、权限、远程连接 |
| 3 | `3. Agent以及AI工具的使用` | Claude Code 等 Agent 的使用方法与最佳实践 |
| 4 | `4. 机器学习基础与Python环境` | Python 环境管理、ML 基础 |
| 5 | `5. 深度学习基础` | 神经网络、训练流程、PyTorch |
| 6 | `6. 机器人基础（ROS2与运动学）` | ROS2、坐标系、运动学 |
| 7 | `7. Lerobot实践` | LeRobot 数据、训练与部署 |
| 8 | `8. VLA论文与实战` | VLA 论文精读与实战 |

## 如何使用本教程

1. 克隆仓库并按章节顺序学习（第 1–3 章是后续所有内容的基础，建议不要跳过）。
2. 每个章节以 `.ipynb` 为主，请在 Jupyter / VS Code 中打开并逐个单元格运行。
3. 遇到问题先自己尝试，再向 Agent 求助。
4. 完成每章末尾的任务后，再进入下一章。

## 环境要求

- 操作系统：Windows、macOS、Linux 均可。Windows 可使用 PowerShell，也可使用 WSL2 / Git Bash（第 1 章同时提供 PowerShell 和 bash 两个版本）
- Python 3.10+
- Git
- Jupyter 或 VS Code（含 Jupyter 扩展）
- 推荐的 Agent 工具：Codex、Claude Code、DeepSeek Harness（任选其一即可，第 3 章会讲如何安装与配置）

具体的依赖与安装步骤将在各章节中给出。

## 与 Agent 一起学习

本仓库的根目录有一份 [AGENTS.md](./AGENTS.md)，它规定了 Agent 在这里应该怎么配合你学习。推荐使用 **Codex、Claude Code、DeepSeek Harness** 之一，其他 Agent 也可以通过它进入下面两种模式。

### 怎么进入

在仓库**根目录**启动你的 Agent（Codex、Claude Code 或 DeepSeek Harness），直接开始对话就行，**不需要输入任何特殊提示词**。Agent 会自动读取 `AGENTS.md`，进入学习者模式，并引导你选择「问答模式」或「答题模式」以及要学习的章节。

如果你发现 Agent 没有按上面的方式引导你，说明它没有读取 `AGENTS.md`，请手动让它阅读根目录的 `AGENTS.md`。

### 两种模式

| 模式 | 用来做什么 | Agent 会怎么做 |
| --- | --- | --- |
| 问答知识点模式 | 学习时遇到疑问 | 解释概念和报错，指出该回看哪一节，给提示但不直接给作业答案 |
| 答题模式 | 检验自己是否掌握了本章 | 出选择题，判分并讲解错题，做完后给你一份总结 |

答题模式需要该章有对应的 `Agent选择题协议.md`，目前第 1 章已开放。

### 所有操作都要你亲手完成

- Agent 只负责讲解、提示和检查你粘贴过来的内容，**不会替你运行命令、写作业文件或提交 Pull Request / Issue**
- 需要让 Agent 了解你的情况时，请自己运行命令，把输出粘贴给它
- 对 Agent 给出的命令，先弄懂再执行，尤其是涉及删除、覆盖、`sudo` 的操作

## 贡献与反馈

- 发现错误或有改进建议，请提交 Issue 或联系 Shiro
- 贡献内容前请阅读 [AGENTS.md](./AGENTS.md) 中的内容编写规范

## 许可

待定（TODO：Shiro 补充）。
