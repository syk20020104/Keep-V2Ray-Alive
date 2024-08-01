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
import json

# 代码1 以下函数用于发送消息到企业微信
def send_wechat_message(webhook_url, message):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    response = requests.post(webhook_url, headers=headers, json=data)
    return response.json()

# 代码1 准备要发送的消息内容
def prepare_message(results):
    message = "SSH命令执行结果汇总：\n"
    for command, hosts in results.items():
        message += f"命令 '{command}' 执行结果：\n"
        for host, output in hosts:
            message += f"{host}: {output}\n"
    return message

# 企业微信的Webhook URL，需要替换成实际的URL
webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e4f4f58a-68f7-45e9-a5ea-a517f6d6f834"

# 代码1 准备消息
message = prepare_message(results)

# 代码1 发送消息到企业微信
if __name__ == "__main__":
    response = send_wechat_message(webhook_url, message)
    print("消息发送状态：", response)


# 代码2 构建消息内容
message_content = "SSH服务器登录信息：\n"
for user in user_list:
    message_content += f"输出内容：\n{user}\n"
message_content += f"\n本次登录用户共：{len(user_list)} 个\n登录时间(北京时间)：{current_time}\n登录IP：{loginip}"

# 以下函数用于 代码2 发送消息到企业微信
def send_wechat_message(webhook_url, message):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    response = requests.post(webhook_url, headers=headers, json=data)
    return response

# 代码2 发送消息到企业微信
# 发送消息到企业微信
if __name__ == "__main__":
    response = send_wechat_message(webhook_url, message_content)
    if response.ok:
        print("消息发送成功。")
    else:
        print("消息发送失败：", response.text)
'''













