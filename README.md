# QQ Chat Desensitizer (QQ聊天记录脱敏工具)

[![AI-Powered](https://img.shields.io/badge/Powered%20by-Gemini%203.1%20Pro-blue?style=flat-square)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

专为将 QQ 聊天记录转化为 **AI 语料（ChatGPT / Claude / Kimi 等）** 而设计的本地清洗与脱敏流水线。

## ⚠️ 兼容性说明 (Compatibility)

本项目目前**仅兼容**由 [qq-chat-exporter](https://github.com/shuakami/qq-chat-exporter) 项目导出的 **JSON 格式**聊天记录文件。程序依赖该项目的特定数据结构进行解析，输入其他格式的 JSON 或文本文件可能会导致处理失败。

## 🎯 核心特性 (Features)

* **精准隐私隐匿:** * 识别并掩码：11位手机号、18位身份证号、银行卡号、电子邮箱地址。
  * 智能处理：将 QQ 号替换为 `[隐藏QQ号]`，并使用前瞻断言确保不误杀时间戳、坐标或日期。
* **关系图谱保护:** 自动将真实昵称映射为“用户1”、“用户2”等标识。采用长昵称优先匹配，确保在隐匿身份的同时保留对话的逻辑流。
* **AI 语料降噪:** 彻底剔除 `[图片: xxx]`、`[语音: xxx]` 等无意义的媒体占位符，大幅降低 AI 的 Token 消耗与注意力干扰。

---

## 🚀 快速开始 (普通用户)

如果你没有 Python 环境，请直接使用打包好的独立程序：

1. 在 [Releases] 页面下载 `qq-cleaner.exe`。
2. 将导出的原始记录重命名为 `export.json`。
3. 将 `qq-cleaner.exe` 与 `export.json` 放在同一文件夹下，**双击运行**即可。
4. 结果将保存为同目录下的 `desensitized_chat.txt`。

---

## 💻 开发者指南 (Python & uv)

本项目使用 `uv` 进行构建与管理。

### 环境初始化

```bash
git clone [https://github.com/YOUR_USERNAME/qq-chat-desensitizer.git](https://github.com/YOUR_USERNAME/qq-chat-desensitizer.git)
cd qq-chat-desensitizer
uv sync
```

### CLI 调用

```bash
uv run qq-cleaner -i export.json -o result.txt
```

---

## 🤖 致谢 (Acknowledgements)

本项目的所有核心逻辑、架构设计及文档编写均由 **Gemini 3.1 Pro** 自动生成完成。

## 📜 许可证 (License)

MIT License
