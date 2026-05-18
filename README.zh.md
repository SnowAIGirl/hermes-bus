# hermes-bus

[English](./README.md) | [中文](./README.zh.md)

通用 Unix Socket 消息总线 — 消息路由、会话管理、心跳。

纯传输层。通知逻辑通过可配置的 hook 注入，总线本身不感知音频、显示或 LLM 上下文。

## 安装

```bash
pip install hermes-bus
```

或从源码安装：

```bash
git clone https://github.com/mlinquan/hermes-bus.git
cd hermes-bus && pip install -e .
```

## CLI

```bash
hermes-busd start       # 启动总线守护进程
hermes-busd stop        # 停止
hermes-busd status      # 查看状态 + 已连接端点
hermes-busd restart     # 重启
hermes-bus-server       # 前台启动（调试用）
```

## Python API

```python
from hermes_bus.client import BusClient, send_message

# 长连接：注册为端点并持续监听消息
client = BusClient("my-service")
client.connect()
for msg in client.poll():
    print(msg)

# 短连接：一次性发送
send_message("target-service", {"text": "hello", "type": "ack"})
```

## 协议

4 字节大端长度前缀 + JSON body。单条消息上限 10MB。

长连接注册端点后可收发消息。短连接发完即断，不注册不占用 endpoint_map。

## Hook

消息路由后异步触发 hook 脚本。优先级：

1. `HERMES_BUS_HOOKS` 环境变量
2. `hooks.yaml` 配置文件
3. 默认自动发现 `hermes-notify/bus_callback.py`

每个 hook 从 stdin 接收完整消息 JSON，不阻塞主消息循环。
