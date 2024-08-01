import os
import paramiko
import json

def ssh_execute_commands(hosts_info, commands):
    overall_results = {}
    for command in commands:
        results = []
        for host_info in hosts_info:
            hostname = host_info['hostname']
            username = host_info['username']
            password = host_info['password']
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname, port=22, username=username, password=password)
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()
                ssh.close()
                if error:
                    results.append((hostname, command, error))
                else:
                    results.append((hostname, command, output))
            except Exception as e:
                print(f"用户：{username}，连接 {hostname} 时出错: {str(e)}")
                results.append((hostname, command, str(e)))
        overall_results[command] = results
    return overall_results

ssh_info_str = os.getenv('SSH_INFO', '[]')  # 从环境变量获取SSH信息
hosts_info = json.loads(ssh_info_str)        # 解析JSON格式的SSH信息

# 要执行的命令列表
# commands = ["/home/syk2002/.npm-global/bin/pm2 list&& pwd", "which pm2"]
commands = ["sh start_v2ray.sh", "uptime"]

# 执行命令并获取结果
results = ssh_execute_commands(hosts_info, commands)

# 打印每个命令的执行结果
for command, command_results in results.items():
    print(f"执行命令 '{command}' 的结果：")
    for hostname, command_executed, result in command_results:
        print(f"服务器 {hostname} 上执行 '{command_executed}' 的结果是: {result}\n")






import requests

# 定义发送企业微信消息的函数
def send_wechat_message(webhook_url, message):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    response = requests.post(webhook_url, headers=headers, json=data)
    if response.ok:
        print("企业微信消息发送成功")
    else:
        print(f"企业微信消息发送失败，状态码：{response.status_code}，错误信息：{response.text}")

# 从环境变量中获取企业微信Webhook URL
wechat_webhook_url = os.getenv('WECHAT_WEBHOOK_URL')

# 设置每条消息的最大长度和每批次的消息数量
MAX_MESSAGE_LENGTH = 1024
BATCH_SIZE = 5

# 准备要发送的消息批次
batches = []
message = ""

for i, (command, command_results) in enumerate(results.items()):
    # 构建每条命令的摘要信息
    summary = f"执行命令 '{command}' 的结果摘要：\n"
    for j, (hostname, _, result) in enumerate(command_results):
        if len(summary) + len(result) > MAX_MESSAGE_LENGTH:
            if j > 0:
                summary += "...（部分结果省略）"
            break
        summary += f"服务器 {hostname}：{result}\n"
    
    # 如果消息过长，则创建新的批次
    if len(message) + len(summary) > MAX_MESSAGE_LENGTH:
        batches.append(message)
        message = summary
    else:
        message += summary + "\n\n"
    
    # 如果达到批次大小，发送当前批次并重置消息
    if (i + 1) % BATCH_SIZE == 0 or i == len(results) - 1:
        batches.append(message)
        message = ""

# 发送所有批次的消息
for batch in batches:
    if wechat_webhook_url:
        send_wechat_message(wechat_webhook_url, batch)
    else:
        print("未设置企业微信Webhook URL，跳过消息发送。")
