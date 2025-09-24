# IDA-RPC

Display what you're disassembling in **IDA Pro** directly on your **Discord Rich Presence** — for **Linux**.

![IDA Pro Rich Presence](https://img.shields.io/badge/discord-rich--presence-blueviolet?logo=discord&style=flat-square)
![Linux Only](https://img.shields.io/badge/platform-linux-lightgrey?logo=linux&style=flat-square)
![Python](https://img.shields.io/badge/python-3.6%2B-blue?logo=python&style=flat-square)

---

## 🔍 What is this?

**IDA-RPC** is a simple Python script that integrates with any version of IDA (Pro, Freeware, Home) with Discord Rich Presence.

When you're disassembling a binary in IDA, your Discord profile will automatically show:
- That you're using IDA
- The name of the binary you're analyzing

> ⚠️ Currently Linux-only, since it uses `xdotool` to grab window titles.

---

## ⚙️ Requirements

- **Python 3.6+**
- `psutil`
- `pypresence`
- `xdotool` (Linux utility for interacting with X windows)

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Clone the repository and run the script:
```
git clone https://github.com/prototypesick/IDA-RPC.git
cd ida-rpc
python -m venv IDA-RPC
source IDA-RPC/bin/activate
pip install -r requirements.txt
python3 ida_rpc.py
```
