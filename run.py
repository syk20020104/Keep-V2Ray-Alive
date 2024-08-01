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
def send_wechat_message(webhook_url, message, page=1, total_pages=None):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": f"{message}\n\n第 {page} 页，共 {total_pages} 页"
        }
    }
    response = requests.post(webhook_url, headers=headers, json=data)
    if response.ok:
        print(f"第 {page} 页消息发送成功")
    else:
        print(f"第 {page} 页消息发送失败，状态码：{response.status_code}，错误信息：{response.text}")

# 从环境变量中获取企业微信Webhook URL
wechat_webhook_url = os.getenv('WECHAT_WEBHOOK_URL')

# 设置每条消息的最大长度
MAX_MESSAGE_LENGTH = 2000  # 假设每条消息最大长度为2000字符

# 准备要发送的消息内容
message = "SSH命令执行结果汇总：\n"
for command, command_results in results.items():
    message += f"执行命令 '{command}' 的结果：\n"
    for hostname, command_executed, result in command_results:
        message += f"服务器 {hostname} 上执行 '{command_executed}' 的结果是: {result}\n"

# 计算总页数
total_length = len(message)
pages = (total_length + MAX_MESSAGE_LENGTH - 1) // MAX_MESSAGE_LENGTH  # 向上取整

# 分割消息内容并发送
for page in range(1, pages + 1):
    start_index = (page - 1) * MAX_MESSAGE_LENGTH
    end_index = start_index + MAX_MESSAGE_LENGTH
    page_content = message[start_index:end_index]
    send_wechat_message(wechat_webhook_url, page_content, page, pages)
