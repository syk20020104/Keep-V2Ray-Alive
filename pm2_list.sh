#!/bin/bash
# 这个脚本用于列出所有PM2管理的进程

# 确保 PATH 环境变量包含 PM2 的路径
export PATH=$PATH:/home/syk2002/.npm-global/bin

# 打印 PM2 进程列表
echo "正在列出所有PM2管理的进程..."
/home/syk2002/.npm-global/bin/pm2 list

echo "PM2进程列表已显示完毕。"
