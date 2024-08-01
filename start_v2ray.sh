#!/bin/bash
# 启动和停止 v2ray 进程的脚本

# 设置 PM2 的路径
export PATH=$PATH:/home/syk2002/.npm-global/bin

# 打印当前 PM2 进程状态
echo "检查 PM2 进程状态..."
pm2 status

# 停止 v2ray 进程，如果成功，则继续启动
echo "尝试停止已存在的 v2ray 进程..."
pm2 stop v2ray && echo "v2ray 进程已停止。" || echo "未找到正在运行的 v2ray 进程。"

# 启动 v2ray 进程
echo "正在启动 v2ray 进程..."
pm2 start ./domains/v2ray/v2ray --name v2ray -- run

# 打印 PM2 进程列表
echo "正在列出所有PM2管理的进程..."
pm2 list

echo "v2ray 进程启动完毕。"
